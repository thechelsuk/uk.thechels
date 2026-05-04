#!/usr/bin/env bash

set -euo pipefail

bundle exec ruby <<'RUBY'
require "jekyll"
require "pathname"

root = Dir.pwd

def normalise_output_path(url)
  path = url.sub(%r{\A/}, "")
  path = path.sub(%r{/index\z}, "")
  path.sub(%r{/\z}, "")
end

def exact_path_exists?(path)
  dir = File.dirname(path)
  base = File.basename(path)
  Dir.exist?(dir) && Dir.children(dir).include?(base)
end

def case_variant(path)
  dir = File.dirname(path)
  base = File.basename(path)
  return nil unless Dir.exist?(dir)

  Dir.children(dir).find do |name|
    name.casecmp?(base) && name != base
  end
end

def relative_to_root(root, path)
  Pathname.new(path).relative_path_from(Pathname.new(root)).to_s
end

site = Jekyll::Site.new(
  Jekyll.configuration(
    "source" => root,
    "destination" => File.join(root, "_site"),
    "config" => "_config.yml"
  )
)

site.read

expected = []

site.posts.docs.each do |doc|
  next unless File.extname(doc.path) == ".md"

  output_path = normalise_output_path(doc.url)
  next if output_path.empty?

  expected << {
    source: relative_to_root(root, doc.path),
    html: File.join(site.dest, "#{output_path}.html"),
    markdown: File.join(site.dest, "#{output_path}.md")
  }
end

missing_html = []
missing_markdown = []
html_case_mismatches = []
markdown_case_mismatches = []

expected.each do |item|
  unless exact_path_exists?(item[:html])
    variant = case_variant(item[:html])
    if variant
      html_case_mismatches << item.merge(actual: File.join(File.dirname(item[:html]), variant))
    else
      missing_html << item
    end
  end

  unless exact_path_exists?(item[:markdown])
    variant = case_variant(item[:markdown])
    if variant
      markdown_case_mismatches << item.merge(actual: File.join(File.dirname(item[:markdown]), variant))
    else
      missing_markdown << item
    end
  end
end

expected_markdown_paths = expected.map { |item| item[:markdown] }.to_h { |path| [path, true] }
orphan_markdown = Dir.glob(File.join(site.dest, "**/*.md")).reject do |path|
  expected_markdown_paths.key?(path)
end.sort

problem_count = missing_html.length + html_case_mismatches.length + missing_markdown.length + markdown_case_mismatches.length + orphan_markdown.length

if problem_count.zero?
  puts "Markdown sibling audit: OK (#{expected.length} expected siblings, no missing files, no case mismatches, no orphans)"
  exit 0
end

puts "Markdown sibling audit: FAIL"
puts "  expected html siblings: #{expected.length}"
puts "  missing html siblings: #{missing_html.length}"
puts "  html case mismatches: #{html_case_mismatches.length}"
puts "  missing markdown siblings: #{missing_markdown.length}"
puts "  markdown case mismatches: #{markdown_case_mismatches.length}"
puts "  orphan markdown files: #{orphan_markdown.length}"

if missing_html.any?
  puts "Missing html siblings:"
  missing_html.first(20).each do |item|
    puts "  #{relative_to_root(root, item[:html])} <= #{item[:source]}"
  end
end

if html_case_mismatches.any?
  puts "HTML case mismatches:"
  html_case_mismatches.first(20).each do |item|
    puts "  expected #{relative_to_root(root, item[:html])} but found #{relative_to_root(root, item[:actual])}"
  end
end

if missing_markdown.any?
  puts "Missing markdown siblings:"
  missing_markdown.first(20).each do |item|
    puts "  #{relative_to_root(root, item[:markdown])} <= #{item[:source]}"
  end
end

if markdown_case_mismatches.any?
  puts "Markdown case mismatches:"
  markdown_case_mismatches.first(20).each do |item|
    puts "  expected #{relative_to_root(root, item[:markdown])} but found #{relative_to_root(root, item[:actual])}"
  end
end

if orphan_markdown.any?
  puts "Orphan markdown files:"
  orphan_markdown.first(20).each do |path|
    puts "  #{relative_to_root(root, path)}"
  end
end
RUBY
