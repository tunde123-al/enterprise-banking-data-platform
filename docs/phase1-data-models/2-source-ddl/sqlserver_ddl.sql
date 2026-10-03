CREATE TABLE dbo.cards (card_id varchar(16) PRIMARY KEY, customer_id varchar(16) NOT NULL, masked_pan varchar(19) NOT NULL, card_type varchar(16) NOT NULL, status varchar(16) NOT NULL);
CREATE TABLE dbo.merchants (merchant_id varchar(16) PRIMARY KEY, merchant_name varchar(200) NOT NULL, category varchar(32) NOT NULL, city varchar(100), country char(2) NOT NULL);
