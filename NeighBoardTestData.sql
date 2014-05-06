INSERT INTO user VALUES (1, "cgallag2", "Caroline Gallagher", "student");
INSERT INTO user VALUES (2, "scusack", "Sydney Cusack", "student");
INSERT INTO user VALUES (3, "sanderso", "Scott Anderson", "faculty");
INSERT INTO user VALUES (4, "rpurcell", "Rita Purcell", "staff");
INSERT INTO user VALUES (5, "kbottomly", "Kim Bottomly", "staff");

INSERT INTO board VALUES (1, "CS Department", 4, "board", "private",  "all");
INSERT INTO members(boardId, userId) VALUES (1, 1);
INSERT INTO members VALUES (1, 2);
INSERT INTO members VALUES (1, 3);

INSERT INTO board VALUES (2, "Community", 5, "board", "public", null);
INSERT INTO board VALUES (3, "Petitions", null, "petition", "public", null);

INSERT INTO board VALUES (4, "Rita’s Feedback", 4, "feedback", "private", "staff");


INSERT INTO form(formId, boardId, created, title, content, creator, type) VALUES (1, 1, "2014-04-04 18:06:00", "Hello", "World! This is a test post.", 1, "post");


INSERT INTO form VALUES (2, 3, "2014-04-03 8:15:00", "More Chocolate!", "Wellesley should give everyone free chocolate on Fridays", 2, "petition");


INSERT INTO comment(commentId, postId, commenterId, content) VALUES (1, 1, 1, "I’m commenting on the test post. Just saying hi!");


INSERT INTO signature(sigId, petitionId, signer) VALUES (1, 2, 2);

INSERT INTO tag(tagId, postId, value) VALUES (1, 1, "testing");

INSERT INTO form(formId, boardId, created, title, content, creator, type) VALUES (3, 4, "2014-04-03 12:00:43", "Hi Rita!", "Thank you for all your hard work!", 1, "feedback");
