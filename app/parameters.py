# A dictionary of HTML class attributes. Keys refer to the HTML class attributes extracted from a single opinion on the website.
selectors = {
    # Select all <span> tags with a "class" attribute equal to "user-post__author-name".
    "author": ["span.user-post__author-name"],
    # Select all <em> tags where the parent is a <span> tag with a "class" attribute equal to "user-post__author-recomendation".
    "recommendation": ["span.user-post__author-recomendation > em"],
    "stars": ["span.user-post__score-count"],
    "content": ["div.user-post__text"],
    "useful": ["button.vote-yes > span"],
    "useless": ["button.vote-no > span"],
    # Select only the first <time> tag where the parent is a <span> tag with a "class" attribute equal to "user-post__published".
    "published": ["span.user-post__published > time:nth-child(1)", "datetime"],
    # Select only the second <time> tag [...].
    "purchased": ["span.user-post__published > time:nth-child(2)", "datetime"],
    # Select only <div> tags with a "class" attribute equal to "review-feature__item" where the <div> tag is preceded by another <div> tag
    # with a "class" attribute ending with a value equal to "positives". ("CSS attribute selectors")
    "pros": ["div[class$=positives] ~ div.review-feature__item", None, True],
    "cons": ["div[class$=negatives] ~ div.review-feature__item", None, True]
}
