drop table if exists users;
drop table if exists skills;
create table users(
	id integer primary key autoincrement,
	name text not null,
	picture text not null,
	company text,
	email text not null,
	phone text not null,
	country text,
	latitude real,
	longitude real,
	isAccepted integer default 0,
	isComing integer default 0,
	needsReimbursement integer default 0
);
create table skills(
	userId integer not null,
	name text not null,
	rating integer not null
);