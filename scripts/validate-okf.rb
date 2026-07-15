# frozen_string_literal: true

require "date"
require "pathname"
require "yaml"

root = Pathname(ARGV.fetch(0, "catalog")).expand_path
abort "OKF bundle does not exist: #{root}" unless root.directory?

errors = []
concept_count = 0
index_count = 0
log_count = 0

parse_frontmatter = lambda do |path, content|
  lines = content.lines
  return [false, nil, content] unless lines.first&.chomp == "---"

  closing_index = lines[1..]&.index { |line| line.chomp == "---" }
  unless closing_index
    errors << "#{path}: unterminated YAML frontmatter"
    next [true, nil, content]
  end

  closing_index += 1
  yaml = lines[1...closing_index].join
  body = lines[(closing_index + 1)..]&.join || ""

  begin
    metadata = YAML.safe_load(
      yaml,
      permitted_classes: [Date, Time],
      aliases: false,
    )
  rescue Psych::Exception => e
    errors << "#{path}: invalid YAML frontmatter: #{e.message.lines.first.chomp}"
    metadata = nil
  end

  [true, metadata, body]
end

validate_index = lambda do |relative, has_frontmatter, metadata, body|
  index_count += 1

  if relative.dirname == Pathname(".")
    if has_frontmatter && metadata != { "okf_version" => "0.1" }
      errors << "#{relative}: root index frontmatter may only declare okf_version: \"0.1\""
    end
  elsif has_frontmatter
    errors << "#{relative}: nested index files must not contain frontmatter"
  end

  lines = body.lines.map(&:chomp)
  first_content = lines.find { |line| !line.strip.empty? }
  errors << "#{relative}: index body must begin with a level-one heading" unless first_content&.match?(/^# \S/)

  errors << "#{relative}: index must contain at least one linked list entry" unless lines.any? { |line| line.match?(/^[*+-] \[[^\]]+\]\([^)]+\)/) }
end

validate_log = lambda do |relative, has_frontmatter, body|
  log_count += 1
  errors << "#{relative}: log files must not contain frontmatter" if has_frontmatter

  lines = body.lines.map(&:chomp)
  first_content = lines.find { |line| !line.strip.empty? }
  errors << "#{relative}: log body must begin with a level-one heading" unless first_content&.match?(/^# \S/)

  malformed_headings = lines.grep(/^## /).reject { |line| line.match?(/^## \d{4}-\d{2}-\d{2}$/) }
  malformed_headings.each { |line| errors << "#{relative}: invalid log date heading #{line.inspect}" }

  dates = lines.map { |line| line[/^## (\d{4}-\d{2}-\d{2})$/, 1] }.compact
  errors << "#{relative}: log must contain at least one ISO 8601 date heading" if dates.empty?

  dates.each do |date|
    Date.iso8601(date)
  rescue Date::Error
    errors << "#{relative}: invalid ISO 8601 date #{date.inspect}"
  end

  errors << "#{relative}: log dates must be newest first" unless dates == dates.sort.reverse

  date_indexes = lines.each_index.select { |index| lines[index].match?(/^## \d{4}-\d{2}-\d{2}$/) }
  date_indexes.each_with_index do |date_index, position|
    section_end = date_indexes[position + 1] || lines.length
    section = lines[(date_index + 1)...section_end]
    next if section.any? { |line| line.match?(/^[*+-] \S/) }

    errors << "#{relative}: log section #{lines[date_index].inspect} has no list entries"
  end
end

root.glob("**/*.md").sort.each do |path|
  relative = path.relative_path_from(root)
  content = path.binread.force_encoding(Encoding::UTF_8)
  unless content.valid_encoding?
    errors << "#{relative}: file is not valid UTF-8"
    next
  end

  has_frontmatter, metadata, body = parse_frontmatter.call(relative, content)

  case path.basename.to_s
  when "index.md"
    validate_index.call(relative, has_frontmatter, metadata, body)
  when "log.md"
    validate_log.call(relative, has_frontmatter, body)
  else
    concept_count += 1
    unless has_frontmatter
      errors << "#{relative}: concept is missing YAML frontmatter"
      next
    end
    unless metadata.is_a?(Hash)
      errors << "#{relative}: concept frontmatter must be a YAML mapping"
      next
    end

    type = metadata["type"]
    errors << "#{relative}: concept type must be a non-empty string" unless type.is_a?(String) && !type.strip.empty?
  end
end

if errors.any?
  warn "OKF v0.1 validation failed with #{errors.length} error(s):"
  errors.each { |error| warn "- #{error}" }
  exit 1
end

puts "OKF v0.1 validation passed: #{concept_count} concepts, #{index_count} indexes, #{log_count} logs"
