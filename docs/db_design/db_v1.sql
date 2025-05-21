CREATE TABLE "users"
(
    "id"              SERIAL PRIMARY KEY,
    "email"           varchar(255) NOT NULL UNIQUE,
    "full_name"       varchar(255) NOT NULL,
    "hashed_password" varchar(255) NOT NULL,
    "role"            varchar(50)  NOT NULL,
    "is_active"       boolean      NOT NULL DEFAULT TRUE,
    "is_superuser"    boolean      NOT NULL DEFAULT FALSE,
    "created_at"      timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at"      timestamp
);

CREATE TABLE "password_reset_tokens"
(
    "id"         SERIAL PRIMARY KEY,
    "token"      varchar(255) NOT NULL UNIQUE,
    "user_id"    int          NOT NULL,
    "expires_at" timestamp    NOT NULL,
    "is_used"    boolean      NOT NULL DEFAULT FALSE,
    "created_at" timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "continents"
(
    "id"               SERIAL PRIMARY KEY,
    "name"             varchar(100) NOT NULL,
    "code"             varchar(10)  NOT NULL UNIQUE,
    "name_code"        varchar(100),
    "background_image" varchar(255),
    "logo"             varchar(255),
    "description"      text,
    "description_code" text,
    "status"           int          NOT NULL DEFAULT 1,
    "created_date"     date         NOT NULL DEFAULT CURRENT_DATE,
    "updated_date"     date
);

CREATE TABLE "countries"
(
    "id"               SERIAL PRIMARY KEY,
    "code"             varchar(10)  NOT NULL UNIQUE,
    "name"             varchar(100) NOT NULL,
    "name_code"        varchar(100),
    "description"      text,
    "description_code" text,
    "background_image" varchar(255),
    "logo"             varchar(255),
    "status"           int          NOT NULL DEFAULT 1,
    "created_date"     date         NOT NULL DEFAULT CURRENT_DATE,
    "updated_date"     date,
    "continent_id"     int          NOT NULL
);

CREATE TABLE "regions"
(
    "id"               SERIAL PRIMARY KEY,
    "name"             varchar(100) NOT NULL,
    "code"             varchar(20)  NOT NULL,
    "name_code"        varchar(100),
    "description"      text,
    "description_code" text,
    "background_image" varchar(255),
    "logo"             varchar(255),
    "status"           int          NOT NULL DEFAULT 1,
    "created_date"     date         NOT NULL DEFAULT CURRENT_DATE,
    "updated_date"     date,
    "country_id"       int          NOT NULL
);

CREATE TABLE "districts"
(
    "id"               SERIAL PRIMARY KEY,
    "name"             varchar(100) NOT NULL,
    "code"             varchar(20)  NOT NULL,
    "name_code"        varchar(100),
    "description"      text,
    "description_code" text,
    "background_image" varchar(255),
    "logo"             varchar(255),
    "status"           int          NOT NULL DEFAULT 1,
    "created_date"     date         NOT NULL DEFAULT CURRENT_DATE,
    "updated_date"     date,
    "region_id"        int          NOT NULL
);

CREATE TABLE "wards"
(
    "id"               SERIAL PRIMARY KEY,
    "name"             varchar(100) NOT NULL,
    "code"             varchar(20)  NOT NULL,
    "name_code"        varchar(100),
    "description"      text,
    "description_code" text,
    "background_image" varchar(255),
    "logo"             varchar(255),
    "status"           int          NOT NULL DEFAULT 1,
    "created_date"     date         NOT NULL DEFAULT CURRENT_DATE,
    "updated_date"     date,
    "district_id"      int          NOT NULL
);

CREATE TABLE "location_categories"
(
    "id"         SERIAL PRIMARY KEY,
    "name"       varchar(100) NOT NULL,
    "status"     boolean      NOT NULL DEFAULT TRUE,
    "created_at" timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp
);

CREATE TABLE "media_type"
(
    "id"           SERIAL PRIMARY KEY,
    "name"         varchar(100) NOT NULL,
    "description"  text,
    "status"       int          NOT NULL DEFAULT 1,
    "created_date" date         NOT NULL DEFAULT CURRENT_DATE,
    "updated_date" date
);

CREATE TABLE "media_category"
(
    "id"           SERIAL PRIMARY KEY,
    "name"         varchar(100) NOT NULL,
    "description"  text,
    "status"       int          NOT NULL DEFAULT 1,
    "created_date" date         NOT NULL DEFAULT CURRENT_DATE,
    "updated_date" date
);

CREATE TABLE "locations"
(
    "id"               SERIAL PRIMARY KEY,
    "name"             varchar(255) NOT NULL,
    "name_code"        varchar(255),
    "description"      text,
    "description_code" text,
    "latitude"         float,
    "longitude"        float,
    "geom"             text,
    "address"          varchar(255),
    "city"             varchar(100),
    "country_id"       int,
    "region_id"        int,
    "district_id"      int,
    "ward_id"          int,
    "category_id"      int          NOT NULL,
    "thumbnail_url"    varchar(255),
    "price_min"        float,
    "price_max"        float,
    "popularity_score" float                 DEFAULT 0,
    "is_active"        boolean      NOT NULL DEFAULT TRUE,
    "created_at"       timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at"       timestamp
);

CREATE TABLE "accommodations_categories"
(
    "id"         SERIAL PRIMARY KEY,
    "name"       varchar(100) NOT NULL,
    "status"     boolean      NOT NULL DEFAULT TRUE,
    "created_at" timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp
);

CREATE TABLE "accommodations"
(
    "id"               SERIAL PRIMARY KEY,
    "user_id"          int          NOT NULL,
    "name"             varchar(255) NOT NULL,
    "name_code"        varchar(255),
    "description"      text,
    "description_code" text,
    "latitude"         float,
    "longitude"        float,
    "geom"             text,
    "address"          varchar(255),
    "city"             varchar(100),
    "country_id"       int,
    "region_id"        int,
    "district_id"      int,
    "ward_id"          int,
    "category_id"      int          NOT NULL,
    "thumbnail_url"    varchar(255),
    "price_min"        float,
    "price_max"        float,
    "popularity_score" float                 DEFAULT 0,
    "checkin_time"     time,
    "checkout_time"    time,
    "cancel_policy"    text,
    "pet_policy"       text,
    "child_policy"     text,
    "is_active"        boolean      NOT NULL DEFAULT TRUE,
    "created_at"       timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at"       timestamp
);

CREATE TABLE "accommodation_rooms"
(
    "id"               SERIAL PRIMARY KEY,
    "accommodation_id" int          NOT NULL,
    "name"             varchar(255) NOT NULL,
    "name_code"        varchar(255),
    "description"      text,
    "description_code" text,
    "adult_capacity"   int          NOT NULL DEFAULT 1,
    "child_capacity"   int                   DEFAULT 0,
    "room_area"        int,
    "bed_capacity"     varchar(100),
    "status"           int          NOT NULL DEFAULT 1,
    "created_at"       timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at"       timestamp
);

CREATE TABLE "ratings"
(
    "id"             SERIAL PRIMARY KEY,
    "reference_id"   int         NOT NULL,
    "reference_type" varchar(50) NOT NULL,
    "user_id"        int         NOT NULL,
    "rating"         float       NOT NULL,
    "comment"        text,
    "created_at"     timestamp   NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE "food_categories"
(
    "id"         SERIAL PRIMARY KEY,
    "name"       varchar(100) NOT NULL,
    "status"     boolean      NOT NULL DEFAULT TRUE,
    "created_at" timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp
);

CREATE TABLE "food"
(
    "id"               SERIAL PRIMARY KEY,
    "name"             varchar(255) NOT NULL,
    "name_code"        varchar(255),
    "description"      text,
    "description_code" text,
    "country_id"       int,
    "region_id"        int,
    "district_id"      int,
    "ward_id"          int,
    "category_id"      int          NOT NULL,
    "thumbnail_url"    varchar(255),
    "price_min"        float,
    "price_max"        float,
    "popularity_score" float                 DEFAULT 0,
    "status"           boolean      NOT NULL DEFAULT TRUE,
    "created_at"       timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at"       timestamp
);

CREATE TABLE "article_categories"
(
    "id"         SERIAL PRIMARY KEY,
    "name"       varchar(100) NOT NULL,
    "status"     boolean      NOT NULL DEFAULT TRUE,
    "created_at" timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp
);

CREATE TABLE "article_tags"
(
    "id"         SERIAL PRIMARY KEY,
    "name"       varchar(100) NOT NULL,
    "name_code"  varchar(100),
    "status"     boolean      NOT NULL DEFAULT TRUE,
    "created_at" timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp
);

CREATE TABLE "article"
(
    "id"               SERIAL PRIMARY KEY,
    "author_id"        int          NOT NULL,
    "title"            varchar(255) NOT NULL,
    "title_code"       varchar(255),
    "description"      text,
    "description_code" text,
    "content"          text         NOT NULL,
    "country_id"       int,
    "region_id"        int,
    "district_id"      int,
    "ward_id"          int,
    "thumbnail_url"    varchar(255),
    "view_count"       int                   DEFAULT 0,
    "status"           boolean      NOT NULL DEFAULT TRUE,
    "created_at"       timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at"       timestamp
);

CREATE TABLE "article_comment"
(
    "id"         SERIAL PRIMARY KEY,
    "user_id"    int       NOT NULL,
    "article_id" int       NOT NULL,
    "content"    text      NOT NULL,
    "status"     boolean   NOT NULL DEFAULT TRUE,
    "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp
);

CREATE TABLE "article_reaction"
(
    "id"         SERIAL PRIMARY KEY,
    "user_id"    int       NOT NULL,
    "article_id" int       NOT NULL,
    "status"     boolean   NOT NULL DEFAULT TRUE,
    "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp
);

CREATE TABLE "article_article_categories"
(
    "id"                    SERIAL PRIMARY KEY,
    "article_id"            int NOT NULL,
    "article_categories_id" int NOT NULL
);

CREATE TABLE "article_article_tags"
(
    "id"              SERIAL PRIMARY KEY,
    "article_id"      int NOT NULL,
    "article_tags_id" int NOT NULL
);

CREATE TABLE "organizer"
(
    "id"               SERIAL PRIMARY KEY,
    "user_id"          int          NOT NULL,
    "name"             varchar(255) NOT NULL,
    "name_code"        varchar(255),
    "description"      text,
    "description_code" text,
    "email"            varchar(255),
    "phone"            varchar(20),
    "website"          varchar(255),
    "status"           boolean      NOT NULL DEFAULT TRUE,
    "created_at"       timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at"       timestamp
);

CREATE TABLE "event_categories"
(
    "id"         SERIAL PRIMARY KEY,
    "name"       varchar(100) NOT NULL,
    "status"     boolean      NOT NULL DEFAULT TRUE,
    "created_at" timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp
);

CREATE TABLE "event"
(
    "id"               SERIAL PRIMARY KEY,
    "user_id"          int          NOT NULL,
    "organizer_id"     int          NOT NULL,
    "category_id"      int          NOT NULL,
    "name"             varchar(255) NOT NULL,
    "name_code"        varchar(255),
    "description"      text,
    "description_code" text,
    "content"          text,
    "country_id"       int,
    "region_id"        int,
    "district_id"      int,
    "ward_id"          int,
    "thumbnail_url"    varchar(255),
    "view_count"       int                   DEFAULT 0,
    "start_time"       time,
    "start_date"       date         NOT NULL,
    "end_date"         date,
    "price"            decimal(10, 2),
    "max_attendees"    int,
    "status"           boolean      NOT NULL DEFAULT TRUE,
    "created_at"       timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at"       timestamp
);

CREATE TABLE "event_attendee"
(
    "id"         SERIAL PRIMARY KEY,
    "user_id"    int       NOT NULL,
    "event_id"   int       NOT NULL,
    "status"     boolean   NOT NULL DEFAULT TRUE,
    "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp
);

CREATE TABLE "event_sponsor"
(
    "id"           SERIAL PRIMARY KEY,
    "organizer_id" int       NOT NULL,
    "event_id"     int       NOT NULL,
    "status"       boolean   NOT NULL DEFAULT TRUE,
    "created_at"   timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at"   timestamp
);

CREATE TABLE "community_post_categories"
(
    "id"               SERIAL PRIMARY KEY,
    "name"             varchar(100) NOT NULL,
    "name_code"        varchar(100),
    "description"      text,
    "description_code" text,
    "status"           boolean      NOT NULL DEFAULT TRUE,
    "created_at"       timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at"       timestamp
);

CREATE TABLE "community_post_tags"
(
    "id"         SERIAL PRIMARY KEY,
    "name"       varchar(100) NOT NULL,
    "status"     boolean      NOT NULL DEFAULT TRUE,
    "created_at" timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp
);

CREATE TABLE "community_post"
(
    "id"            SERIAL PRIMARY KEY,
    "user_id"       int          NOT NULL,
    "category_id"   int          NOT NULL,
    "title"         varchar(255) NOT NULL,
    "content"       text         NOT NULL,
    "thumbnail_url" varchar(255),
    "view_count"    int                   DEFAULT 0,
    "status"        boolean      NOT NULL DEFAULT TRUE,
    "created_at"    timestamp    NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at"    timestamp
);

CREATE TABLE "community_post_community_post_tags"
(
    "id"                    SERIAL PRIMARY KEY,
    "community_post_id"     int NOT NULL,
    "community_post_tag_id" int NOT NULL
);

CREATE TABLE "community_post_comment"
(
    "id"         SERIAL PRIMARY KEY,
    "user_id"    int       NOT NULL,
    "post_id"    int       NOT NULL,
    "content"    text      NOT NULL,
    "parent_id"  int,
    "status"     boolean   NOT NULL DEFAULT TRUE,
    "created_at" timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" timestamp
);

CREATE TABLE "community_post_reaction"
(
    "id"            SERIAL PRIMARY KEY,
    "user_id"       int         NOT NULL,
    "post_id"       int         NOT NULL,
    "reaction_type" varchar(20) NOT NULL,
    "comment_id"    int,
    "status"        boolean     NOT NULL DEFAULT TRUE,
    "created_at"    timestamp   NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at"    timestamp
);

CREATE TABLE "media"
(
    "id"             SERIAL PRIMARY KEY,
    "type_id"        int         NOT NULL,
    "category_id"    int         NOT NULL,
    "reference_id"   int         NOT NULL,
    "reference_type" varchar(50) NOT NULL,
    "url"            text        NOT NULL,
    "title"          varchar(255),
    "description"    text,
    "status"         int         NOT NULL DEFAULT 1,
    "created_date"   date        NOT NULL DEFAULT CURRENT_DATE,
    "updated_date"   date
);

ALTER TABLE "password_reset_tokens"
    ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "countries"
    ADD FOREIGN KEY ("continent_id") REFERENCES "continents" ("id");

ALTER TABLE "regions"
    ADD FOREIGN KEY ("country_id") REFERENCES "countries" ("id");

ALTER TABLE "districts"
    ADD FOREIGN KEY ("region_id") REFERENCES "regions" ("id");

ALTER TABLE "wards"
    ADD FOREIGN KEY ("district_id") REFERENCES "districts" ("id");

ALTER TABLE "locations"
    ADD FOREIGN KEY ("country_id") REFERENCES "countries" ("id");

ALTER TABLE "locations"
    ADD FOREIGN KEY ("region_id") REFERENCES "regions" ("id");

ALTER TABLE "locations"
    ADD FOREIGN KEY ("district_id") REFERENCES "districts" ("id");

ALTER TABLE "locations"
    ADD FOREIGN KEY ("ward_id") REFERENCES "wards" ("id");

ALTER TABLE "locations"
    ADD FOREIGN KEY ("category_id") REFERENCES "location_categories" ("id");

ALTER TABLE "media"
    ADD FOREIGN KEY ("type_id") REFERENCES "media_type" ("id");

ALTER TABLE "media"
    ADD FOREIGN KEY ("category_id") REFERENCES "media_category" ("id");

ALTER TABLE "media"
    ADD FOREIGN KEY ("reference_id") REFERENCES "locations" ("id");

ALTER TABLE "accommodations"
    ADD FOREIGN KEY ("category_id") REFERENCES "accommodations_categories" ("id");

ALTER TABLE "media"
    ADD FOREIGN KEY ("reference_id") REFERENCES "accommodations" ("id");

ALTER TABLE "accommodation_rooms"
    ADD FOREIGN KEY ("accommodation_id") REFERENCES "accommodations" ("id");

ALTER TABLE "accommodations"
    ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "ratings"
    ADD FOREIGN KEY ("reference_id") REFERENCES "locations" ("id");

ALTER TABLE "ratings"
    ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "media"
    ADD FOREIGN KEY ("reference_id") REFERENCES "food" ("id");

ALTER TABLE "food"
    ADD FOREIGN KEY ("category_id") REFERENCES "food_categories" ("id");

ALTER TABLE "ratings"
    ADD FOREIGN KEY ("reference_id") REFERENCES "food" ("id");

ALTER TABLE "article"
    ADD FOREIGN KEY ("author_id") REFERENCES "users" ("id");

ALTER TABLE "article_comment"
    ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "article_comment"
    ADD FOREIGN KEY ("article_id") REFERENCES "article" ("id");

ALTER TABLE "article_reaction"
    ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "article_reaction"
    ADD FOREIGN KEY ("article_id") REFERENCES "article" ("id");

ALTER TABLE "article_article_categories"
    ADD FOREIGN KEY ("article_id") REFERENCES "article" ("id");

ALTER TABLE "article_article_categories"
    ADD FOREIGN KEY ("article_categories_id") REFERENCES "article_categories" ("id");

ALTER TABLE "article_article_tags"
    ADD FOREIGN KEY ("article_id") REFERENCES "article" ("id");

ALTER TABLE "article_article_tags"
    ADD FOREIGN KEY ("article_tags_id") REFERENCES "article_tags" ("id");

ALTER TABLE "media"
    ADD FOREIGN KEY ("reference_id") REFERENCES "organizer" ("id");

ALTER TABLE "organizer"
    ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "media"
    ADD FOREIGN KEY ("reference_id") REFERENCES "event" ("id");

ALTER TABLE "event"
    ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "event"
    ADD FOREIGN KEY ("organizer_id") REFERENCES "organizer" ("id");

ALTER TABLE "event"
    ADD FOREIGN KEY ("category_id") REFERENCES "event_categories" ("id");

ALTER TABLE "event_attendee"
    ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "event_attendee"
    ADD FOREIGN KEY ("event_id") REFERENCES "event" ("id");

ALTER TABLE "event_sponsor"
    ADD FOREIGN KEY ("organizer_id") REFERENCES "organizer" ("id");

ALTER TABLE "event_sponsor"
    ADD FOREIGN KEY ("event_id") REFERENCES "event" ("id");

ALTER TABLE "community_post"
    ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "community_post"
    ADD FOREIGN KEY ("category_id") REFERENCES "community_post_categories" ("id");

ALTER TABLE "community_post_community_post_tags"
    ADD FOREIGN KEY ("community_post_id") REFERENCES "community_post" ("id");

ALTER TABLE "community_post_community_post_tags"
    ADD FOREIGN KEY ("community_post_tag_id") REFERENCES "community_post_tags" ("id");

ALTER TABLE "community_post_comment"
    ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "community_post_comment"
    ADD FOREIGN KEY ("post_id") REFERENCES "community_post" ("id");

ALTER TABLE "community_post_comment"
    ADD FOREIGN KEY ("parent_id") REFERENCES "community_post_comment" ("id");

ALTER TABLE "community_post_reaction"
    ADD FOREIGN KEY ("user_id") REFERENCES "users" ("id");

ALTER TABLE "community_post_reaction"
    ADD FOREIGN KEY ("post_id") REFERENCES "community_post" ("id");

ALTER TABLE "community_post_reaction"
    ADD FOREIGN KEY ("comment_id") REFERENCES "community_post_comment" ("id");

-- Indexes for better performance
CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_locations_coordinates ON locations (latitude, longitude);
CREATE INDEX idx_accommodations_coordinates ON accommodations (latitude, longitude);
CREATE INDEX idx_countries_continent ON countries (continent_id);
CREATE INDEX idx_regions_country ON regions (country_id);
CREATE INDEX idx_districts_region ON districts (region_id);
CREATE INDEX idx_wards_district ON wards (district_id);
CREATE INDEX idx_media_reference ON media (reference_id, reference_type);
CREATE INDEX idx_ratings_reference ON ratings (reference_id, reference_type);
CREATE INDEX idx_community_post_comment_parent ON community_post_comment (parent_id);
