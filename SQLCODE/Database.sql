CREATE TABLE article (
    id VARCHAR(10) PRIMARY KEY,
	title VARCHAR(255) NOT NULL,
    title_summary VARCHAR(255) NOT NULL,
    image_title_url VARCHAR(500),
    author VARCHAR(50),
    create_date DATE,
    comment_count INTEGER DEFAULT 0,
    like_count INTEGER DEFAULT 0,
	type VARCHAR(50),
    summary TEXT,
    content TEXT,
	views INTEGER DEFAULT 0
);

CREATE TABLE article_hots (
    id VARCHAR(10) PRIMARY KEY,
	article_id VARCHAR(10) REFERENCES article(id)
);


CREATE TABLE advertisement (
    id VARCHAR(10) PRIMARY KEY,
    content TEXT
);
