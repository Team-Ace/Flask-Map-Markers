drop table if exists entries;
create table entries (
	id integer primary key autoincrement,
	marker text not null,
	'latlong' text not null
);
