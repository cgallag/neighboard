drop table if exists user;
drop table if exists form;
drop table if exists tag;
drop table if exists signature;
drop table if exists comment;
drop table if exists board;
drop table if exists members;
drop table if exists picfile;

#houses all user types
create table user(
	userId int,
	username char(8),
	name varchar(100),
	primary key (userId),
	unique (userId),
	category enum("student", "faculty", "staff")
);

#includes posts, petitions, and feedback
create table form( 
	formId int auto_increment,
	boardId int, 
	created datetime,
	title varchar(200),
	content varchar(1000),
	creator int,
	type enum("petition", "post", "feedback"),
	primary key (formId),
	foreign key (boardId) references board,
	foreign key (creator) references user
);

# Tags apply only to posts.
create table tag(
	tagId int auto_increment,
	postId int,
	value varchar(50),
	primary key (tagId),
	foreign key (postId) references form
);

# Signatures apply only to petitions.
create table signature(
	sigId int auto_increment,
	petitionId int,
	signer int,
	primary key (sigId),
	foreign key (petitionId) references form,
	foreign key (signer) references user
);

# Post id can apply to either a post or a petition.
create table comment(
	commentId int auto_increment,
	postId int,
	commenterId int,
	content varchar(1000),
	primary key (commentId),
	foreign key (postId) references form,
	foreign key (commenterId) references user
);

# All of the following tables relate to boards.
create table board(
	boardId int auto_increment,
	name varchar(100),
	mailname varchar(120),
	owner int,
	type enum("petition", "board", "feedback"),
	privacyLevel enum("public", "private"),
	category enum("student", "faculty", "staff", "all"),
	primary key (boardId),
	foreign key (owner) references user
);

create table members(
	boardId int,
	userId int,
	foreign key (userId) references user,
	foreign key (boardId) references board
);

create table picfile(
  postId int,
  picUrl varchar(256),
  foreign key (postId) references form
);

create table usersessions(
  sessionkey varchar(256),
  username char(8),
  unique(username)
);