import unittest

from caption_writer import (PLATFORMS, captions, generate_captions,
                            make_hashtags)


class TestHashtags(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(make_hashtags(["减脂", "快手"], 5), ["#减脂", "#快手"])

    def test_dedup_and_limit(self):
        tags = make_hashtags(["减脂", "减脂", "快手", "早餐"], 2)
        self.assertEqual(tags, ["#减脂", "#快手"])

    def test_strip_hash(self):
        self.assertEqual(make_hashtags(["#美食"], 3), ["#美食"])


class TestCaptions(unittest.TestCase):
    def test_multiple_versions(self):
        result = generate_captions("早餐机食谱", "x")
        self.assertEqual(len(result), len(PLATFORMS["x"]["templates"]))

    def test_topic_in_caption(self):
        result = generate_captions("早餐机食谱", "weibo")
        for c in result:
            self.assertIn("早餐机食谱", c)

    def test_hashtag_appended(self):
        result = generate_captions("早餐机食谱", "xiaohongshu", ["减脂", "快手"])
        self.assertTrue(any("#减脂" in c for c in result))

    def test_hashtag_respects_limit(self):
        result = generate_captions("T", "x", ["a", "b", "c", "d", "e"])
        self.assertLessEqual(result[0].count("#"), 3)

    def test_invalid_platform(self):
        with self.assertRaises(ValueError):
            generate_captions("T", "myspace")

    def test_empty_topic(self):
        with self.assertRaises(ValueError):
            generate_captions("  ", "x")

    def test_captions_no_llm(self):
        result = captions("远程协作", "linkedin", use_llm=False)
        self.assertGreater(len(result), 0)


if __name__ == "__main__":
    unittest.main()
