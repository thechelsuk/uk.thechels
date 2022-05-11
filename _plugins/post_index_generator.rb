module Jekyll
    # add post number
    # frozen_string_literal: true
    class PostIndex < Generator
        safe true
        priority :low
        def generate(site)
            site.posts.each_with_index do |item, index|
                item.data["index"] = index
            end
        end
    end
end
