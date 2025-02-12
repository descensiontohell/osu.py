from osu import UserBeatmapType


class TestBeatmap:
    def test_get_beatmap(self, client, sample_beatmap):
        beatmap = client.get_beatmap(sample_beatmap["id"])
        assert beatmap.id == sample_beatmap["id"]
        assert beatmap.beatmapset.title == sample_beatmap["title"]
        assert beatmap.beatmapset.artist == sample_beatmap["artist"]

    def test_get_beatmap_attributes(self, client, sample_beatmap):
        attributes = client.get_beatmap_attributes(sample_beatmap["id"])
        assert attributes.max_combo == sample_beatmap["max_combo"]
        assert attributes.type == sample_beatmap["type"]

    def test_get_beatmaps(self, client, sample_beatmaps):
        beatmaps = client.get_beatmaps([beatmap["id"] for beatmap in sample_beatmaps])
        assert beatmaps
        for beatmap in beatmaps:
            keys = sample_beatmaps[0].keys()
            assert {key: getattr(beatmap, key) for key in keys} in sample_beatmaps

    def test_get_beatmap_scores(self, client, sample_scores):
        scores = client.get_beatmap_scores(sample_scores["beatmap_id"])
        for received_score, sample_score in zip(scores.scores[:3], sample_scores["scores"]):
            assert received_score.id == sample_score["id"]
            assert received_score.user_id == sample_score["user_id"]
            assert received_score.max_combo == sample_score["max_combo"]

    def test_get_user_beatmap_score(self, client, sample_user_beatmap_score):
        score = (client.get_user_beatmap_score(
            beatmap=sample_user_beatmap_score["beatmap_id"],
            user=sample_user_beatmap_score["user_id"],
        )).score
        assert score
        assert score.user_id == sample_user_beatmap_score["user_id"]
        assert score.accuracy == sample_user_beatmap_score["accuracy"]

    def test_get_user_beatmap_scores(self, client, sample_user_beatmap_scores):
        scores = client.get_user_beatmap_scores(
            beatmap=sample_user_beatmap_scores["beatmap_id"],
            user=sample_user_beatmap_scores["user_id"],
        )
        assert scores
        for score in scores:
            keys = sample_user_beatmap_scores["scores"][0].keys()
            assert {key: getattr(score, key) for key in keys} in sample_user_beatmap_scores["scores"]

    def test_search_beatmapsets(self, client):
        # Is undocumented
        ...

    def test_get_beatmapset_discussion_posts(self, client, sample_beatmapset_discussion_post):
        data = client.get_beatmapset_discussion_posts(
            beatmapset_discussion_id=sample_beatmapset_discussion_post["id"]
        )
        assert data
        assert data["posts"]
        assert len(data["beatmapsets"]) == 1
        beatmapset = data["beatmapsets"][0]
        assert beatmapset.title == sample_beatmapset_discussion_post["beatmapset_title"]
        assert beatmapset.artist == sample_beatmapset_discussion_post["beatmapset_artist"]
        target_post = None
        for post in data["posts"]:
            if (
                    post.user_id == sample_beatmapset_discussion_post["target_user"] and
                    post.message == sample_beatmapset_discussion_post["target_message"]
            ):
                target_post = post
        assert target_post

    def test_get_beatmapset_discussion_votes(self, client, sample_beatmapset_discussion_post):
        data = client.get_beatmapset_discussion_votes(sample_beatmapset_discussion_post["id"])
        assert data["votes"]
        target_vote = data["votes"][0]
        assert target_vote.beatmapset_discussion_id == sample_beatmapset_discussion_post["id"]
        assert target_vote.score == 1

    def test_get_beatmapset_discussions(self, client, sample_beatmapset_discussion_post):
        data = client.get_beatmapset_discussions(
            beatmapset_id=sample_beatmapset_discussion_post["beatmapset_id"]
        )
        assert data
        assert data["discussions"]
        target_post = None
        for discussion in data["discussions"]:
            if (
                    discussion.starting_post.user_id == sample_beatmapset_discussion_post["discussion_user"] and
                    discussion.starting_post.message == sample_beatmapset_discussion_post["discussion_message"]
            ):
                target_post = discussion.starting_post
        assert target_post

    def test_lookup_beatmap(self, client, sample_beatmap):
        beatmap = client.lookup_beatmap(checksum=sample_beatmap["md5_sum"])
        assert beatmap
        assert beatmap.beatmapset.title == sample_beatmap["title"]
        assert beatmap.beatmapset.artist == sample_beatmap["artist"]
        assert beatmap.id == sample_beatmap["id"]
