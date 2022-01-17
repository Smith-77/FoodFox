DROP TABLE IF EXISTS recipes;

CREATE TABLE recipes (
    recipe_url TEXT PRIMARY KEY NOT NULL,
    source_url TEXT NOT NULL,
    updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    rating REAL,
    star_rating REAL,
    ratings INTEGER,
    author TEXT,
    ingredients TEXT,
    number_of_ingredients INTEGER,
    instructions TEXT,
    time_in_minutes INTEGER,
    string_time TEXT
);

CREATE TABLE recipes_long (
    recipe_url TEXT PRIMARY KEY NOT NULL,
    source_url TEXT NOT NULL,
    updated TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    rating REAL,
    star_rating REAL,
    ratings INTEGER,
    author TEXT,
    ingredients TEXT,
    number_of_ingredients INTEGER,
    instructions TEXT,
    time_in_minutes INTEGER,
    string_time TEXT
);