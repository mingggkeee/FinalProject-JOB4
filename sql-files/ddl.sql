CREATE TABLE IF NOT EXISTS USER (
  id           VARCHAR(20) NOT NULL PRIMARY KEY,
  password     VARCHAR(1000) NOT NULL,
  birth        DATE,
  email        VARCHAR(40),
  phone_number VARCHAR(12),
  address      VARCHAR(100),
  gender       INTEGER,
  username     VARCHAR(20) NOT NULL DEFAULT 'annonymous',
  is_active    BOOLEAN DEFAULT 1,
  is_admin     BOOLEAN DEFAULT 0,
  last_login    DATETIME,
);

-- CREATE TABLE IF NOT EXISTS myauth_user (
--   id           VARCHAR(20) NOT NULL PRIMARY KEY,
--   password     VARCHAR(1000) NOT NULL,
--   birth        DATE,
--   email        VARCHAR(40),
--   phone_number VARCHAR(12),
--   address      VARCHAR(100),
--   gender       INTEGER,
--     username     VARCHAR(20) NOT NULL DEFAULT 'annonymous',
--   is_active    BOOLEAN DEFAULT 1,
--   is_admin     BOOLEAN DEFAULT 0,
--   last_login    DATETIME
-- );

CREATE TABLE IF NOT EXISTS INDUSTRY (
  industry_id INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  name        VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS QUESTION (
  question_id INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  content     VARCHAR(300)
);

CREATE TABLE IF NOT EXISTS TASK (
  task_id INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  name    VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS INTEREST (
  interest_id INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  id          VARCHAR(20) NOT NULL,
  name        VARCHAR(20),
  FOREIGN KEY (id) REFERENCES USER (id)
);

CREATE TABLE IF NOT EXISTS COMPANY (
  company_id  INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  name        VARCHAR(20) NOT NULL,
  industry_id INTEGER NOT NULL,
  FOREIGN KEY (industry_id) REFERENCES INDUSTRY (industry_id)
);

CREATE TABLE IF NOT EXISTS LETTER (
  letter_id   INTEGER AUTO_INCREMENT NOT NULL PRIMARY KEY,
  content     VARCHAR(10000),
  company_id  INTEGER,
  task_id     INTEGER,
  question_id INTEGER,
  FOREIGN KEY (company_id) REFERENCES COMPANY (company_id),
  FOREIGN KEY (task_id) REFERENCES TASK (task_id),
  FOREIGN KEY (question_id) REFERENCES QUESTION (question_id)
);

CREATE TABLE IF NOT EXISTS BOOKMARK (
  id        VARCHAR(20) NOT NULL,
  letter_id INTEGER NOT NULL,
  PRIMARY KEY (id, letter_id),
  FOREIGN KEY (id) REFERENCES USER (id),
  FOREIGN KEY (letter_id) REFERENCES LETTER (letter_id)
);
