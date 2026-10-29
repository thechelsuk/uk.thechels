import yaml

import fetch_videos


class Entry(dict):
    """Minimal stand-in for a feedparser entry (dict keys + attributes)."""

    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError as e:
            raise AttributeError(name) from e


def make_entry(**overrides):
    entry = Entry(
        title="Opiuml: podcast player out now",
        link="https://www.youtube.com/shorts/SA4JdFof5sA",
        published="2026-10-24T19:41:41+00:00",
        yt_videoid="SA4JdFof5sA",
        media_thumbnail=[{
            "url": "https://i4.ytimg.com/vi/SA4JdFof5sA/hqdefault.jpg",
            "width": "480",
            "height": "360"
        }],
        summary=(
            "In the App Store now\n\n"
            "https://apps.apple.com/us/app/opiuml-podcast-player/id6823693348"
        ),
    )
    entry.update(overrides)
    return entry


def front_matter(text):
    return yaml.safe_load(text.split("---")[1])


class TestVideoDetails:

    def test_video_id_comes_from_feed_field(self):
        entry = make_entry(link="https://example.com/no-id-here")
        assert fetch_videos.get_video_id(entry) == "SA4JdFof5sA"

    def test_video_id_falls_back_to_link(self):
        entry = make_entry(yt_videoid=None,
                           link="https://www.youtube.com/watch?v=z3emy5JtmTQ")
        assert fetch_videos.get_video_id(entry) == "z3emy5JtmTQ"

    def test_shorts_are_flagged(self):
        assert fetch_videos.is_short(make_entry()) is True
        assert fetch_videos.is_short(
            make_entry(
                link="https://www.youtube.com/watch?v=z3emy5JtmTQ")) is False

    def test_thumbnail_from_feed(self):
        assert fetch_videos.get_thumbnail(make_entry()) == (
            "https://i4.ytimg.com/vi/SA4JdFof5sA/hqdefault.jpg")

    def test_thumbnail_falls_back_to_video_id(self):
        entry = make_entry(media_thumbnail=[])
        assert fetch_videos.get_thumbnail(entry) == (
            "https://i.ytimg.com/vi/SA4JdFof5sA/hqdefault.jpg")


class TestDescription:

    def test_bare_urls_become_links(self):
        md = fetch_videos.description_to_markdown(
            "See https://example.com/app for more")
        assert md == "See <https://example.com/app> for more"

    def test_paragraphs_are_kept(self):
        md = fetch_videos.description_to_markdown("One\n\n\n\nTwo\nThree")
        assert md == "One\n\nTwo  \nThree"

    def test_leading_hashtags_do_not_become_headings(self):
        md = fetch_videos.description_to_markdown("#1 tip for pacing")
        assert md == "\\#1 tip for pacing"

    def test_empty_description(self):
        assert fetch_videos.description_to_markdown(None) == ""
        assert fetch_videos.description_to_markdown("   \n ") == ""


class TestPost:

    def test_front_matter_has_video_details(self):
        fm = front_matter(fetch_videos.create_front_matter(make_entry()))
        assert fm["video_id"] == "SA4JdFof5sA"
        assert fm["short"] is True
        assert fm[
            "image"] == "https://i4.ytimg.com/vi/SA4JdFof5sA/hqdefault.jpg"
        assert fm["type"] == "video"
        assert fm["layout"] == "post"

    def test_titles_with_quotes_stay_valid_yaml(self):
        fm = front_matter(
            fetch_videos.create_front_matter(make_entry(title='Say "hi"')))
        assert fm["title"] == 'Say "hi"'

    def test_body_has_description_then_link(self):
        body = fetch_videos.generate_body(make_entry())
        assert body.startswith(
            "In the App Store now\n\n<https://apps.apple.com/")
        assert body.rstrip().endswith(
            "[Watch on YouTube](https://www.youtube.com/shorts/SA4JdFof5sA)")

    def test_body_without_description_is_just_the_link(self):
        body = fetch_videos.generate_body(make_entry(summary=""))
        assert body == "[Watch on YouTube](https://www.youtube.com/shorts/SA4JdFof5sA)\n"


class TestBackfill:

    def test_thin_post_is_upgraded(self):
        old = (
            '---\ntitle: "Opiuml: podcast player out now"\n'
            'seo_title: "x"\nseo_description: "y"\ndate: "2026-10-24"\n'
            'layout: post\nsource: "https://www.youtube.com/shorts/SA4JdFof5sA"\n'
            'type: video\n---\n\n'
            '[Watch on Youtube](https://www.youtube.com/shorts/SA4JdFof5sA)\n')
        new = fetch_videos.backfill_post(old, make_entry())
        fm = front_matter(new)
        assert fm["seo_title"] == "x"  # existing fields are kept
        assert fm["video_id"] == "SA4JdFof5sA"
        assert fm["short"] is True
        assert "In the App Store now" in new
        assert new.count("Watch on YouTube") == 1

    def test_post_with_own_text_is_left_alone(self):
        old = (
            '---\ntitle: "t"\ntype: video\n---\n\nMy own words.\n\n'
            '[Watch on Youtube](https://www.youtube.com/shorts/SA4JdFof5sA)\n')
        assert fetch_videos.backfill_post(old, make_entry()) is None

    def test_already_backfilled_post_is_left_alone(self):
        once = fetch_videos.backfill_post(
            '---\ntitle: "t"\ntype: video\n---\n\n'
            '[Watch on Youtube](https://www.youtube.com/shorts/SA4JdFof5sA)\n',
            make_entry())
        assert fetch_videos.backfill_post(once, make_entry()) is None


class TestCleanTitle:

    def test_trailing_hashtags_are_dropped(self):
        assert fetch_videos.clean_title("Fractions #shorts") == "Fractions"
        assert fetch_videos.clean_title(
            "Christmas Maths Pack #shorts #christmas #maths #worksheets, "
            "#colour #number #maths #advent #mltply") == "Christmas Maths Pack"
        assert fetch_videos.clean_title(
            "New on Cheltenham Open Data - Ward level data! "
            "#cheltenham #cheltenhamtown") == (
                "New on Cheltenham Open Data - Ward level data!")

    def test_hashtags_inside_the_title_keep_their_word(self):
        assert fetch_videos.clean_title(
            "Lighting the way | #thechelsuk on #Twitch") == (
                "Lighting the way | thechelsuk on Twitch")
        assert fetch_videos.clean_title(
            "Cheapest fuel in town #Cheltenham by http://cheltenham-od.uk "
            "#cheltenhamtown") == (
                "Cheapest fuel in town Cheltenham by http://cheltenham-od.uk")

    def test_plain_titles_are_unchanged(self):
        assert fetch_videos.clean_title("Opiuml: podcast player out now"
                                        ) == "Opiuml: podcast player out now"

    def test_new_posts_use_the_clean_title(self):
        entry = make_entry(title="Fractions #shorts")
        fm = front_matter(fetch_videos.create_front_matter(entry))
        assert fm["title"] == "Fractions"
        assert "#" not in fm["seo_title"]
        assert "#" not in fm["seo_description"]
        _, _, filename = fetch_videos.process_entry(entry)
        assert "shorts" not in filename

    def test_existing_title_fields_are_cleaned(self):
        old = ('---\ntitle: "Fractions #shorts"\n'
               'seo_title: "Fractions #shorts - Video"\n'
               'seo_description: "Hand written, keep me."\n'
               'type: video\n---\n\nBody #kept\n')
        new = fetch_videos.clean_title_fields(old)
        fm = front_matter(new)
        assert fm["title"] == "Fractions"
        assert fm["seo_title"] == fetch_videos.seo_fields("Fractions")[0]
        assert fm["seo_description"] == "Hand written, keep me."
        assert new.endswith("Body #kept\n")
        assert fetch_videos.clean_title_fields(new) is None


class TestDescriptionHashtags:

    def test_hashtag_only_lines_are_dropped(self):
        md = fetch_videos.description_to_markdown(
            "Out now\n\n#fractions #worksheets #Shorts")
        assert md == "Out now"


class TestGeneratedSeoFields:

    def test_generated_seo_fields_without_hashes_are_regenerated(self):
        old_title = "Fractions #shorts #maths"
        seo_title, seo_description = fetch_videos.seo_fields(old_title)
        assert "#" not in seo_title  # the generator already drops "#"
        old = (f'---\ntitle: "{old_title}"\n'
               f'seo_title: "{seo_title}"\n'
               f'seo_description: "{seo_description}"\n'
               'type: video\n---\n\nBody\n')
        fm = front_matter(fetch_videos.clean_title_fields(old))
        assert (fm["seo_title"],
                fm["seo_description"]) == fetch_videos.seo_fields("Fractions")
