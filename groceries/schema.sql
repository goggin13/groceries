DROP TABLE IF EXISTS items;
DROP TABLE IF EXISTS categories;

CREATE TABLE items (
  id serial,
  name TEXT UNIQUE NOT NULL
);

CREATE TABLE categories (
    id serial,
    name TEXT UNIQUE NOT NULL
);
