-- migrate:up
CREATE TABLE "users" (
  "rcs_id" varchar PRIMARY KEY,
  "first_name" varchar NOT NULL,
  "last_name" varchar NOT NULL,
  "graduation_year" int,
  "discord_user_id" int
);

COMMENT ON COLUMN "users"."rcs_id" IS 'RPI username of user from CAS';

COMMENT ON COLUMN "users"."first_name" IS 'Given name of user';

COMMENT ON COLUMN "users"."last_name" IS 'Family name of user';

COMMENT ON COLUMN "users"."graduation_year" IS 'Null for non-students hopefully';

COMMENT ON COLUMN "users"."discord_user_id" IS 'Unique ID of Discord user once connected';

-- migrate:down

DROP TABLE "users";