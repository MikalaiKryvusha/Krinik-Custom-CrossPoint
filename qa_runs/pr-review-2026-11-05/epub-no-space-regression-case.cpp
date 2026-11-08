TEST_F(ChapterAnchorPageTest, InlineTargetImmediatelyAfterALongImagePlaceholderFollowsItsText) {
  parser.imageRendering = 1;
  open("p", nullptr);
  const auto alt = words(13 * 8);
  const XML_Char* image[] = {"src", "missing.png", "alt", alt.c_str(), nullptr};
  ChapterHtmlSlimParser::startElement(&parser, "img", image);
  close("img");
  const XML_Char* anchor[] = {"id", "after", nullptr};
  ChapterHtmlSlimParser::startElement(&parser, "a", anchor);
  close("a");
  text("TARGET");
  close("p");
  ASSERT_TRUE(parser.finishParse());
  ASSERT_TRUE(pageOfWord("TARGET").has_value());
  EXPECT_EQ(anchorPage("after"), pageOfWord("TARGET"));
}

