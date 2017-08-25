-- Table: performance.account

-- DROP TABLE performance.account;

CREATE TABLE performance.account
(
    account_id bigint NOT NULL,
    account_name character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT acc_pk PRIMARY KEY (account_id)
)

-- Table: performance.account_attr

-- DROP TABLE performance.account_attr;

CREATE TABLE performance.account_attr
(
    account_id bigint,
    eff_dt date,
    fund_id character varying(30) COLLATE pg_catalog."default",
    stock_selection numeric(20, 10),
    CONSTRAINT attr_acc_fk FOREIGN KEY (account_id)
        REFERENCES performance.account (account_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT attr_fund_fk FOREIGN KEY (fund_id)
        REFERENCES performance.mutual_fund (fund_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)

-- Table: performance.account_info

-- DROP TABLE performance.account_info;

CREATE TABLE performance.account_info
(
    account_id bigint,
    eff_dt date,
    fund_id character varying(30) COLLATE pg_catalog."default",
    weight numeric(20, 10),
    units numeric(20, 10),
    CONSTRAINT atti_acc_fk FOREIGN KEY (account_id)
        REFERENCES performance.account (account_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT atti_fund_fk FOREIGN KEY (fund_id)
        REFERENCES performance.mutual_fund (fund_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)

-- Table: performance.mf_nav

-- DROP TABLE performance.mf_nav;

CREATE TABLE performance.mf_nav
(
    eff_dt date,
    fund_id character varying(30) COLLATE pg_catalog."default",
    nav character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT mf_nav_fund_fk FOREIGN KEY (fund_id)
        REFERENCES performance.mutual_fund (fund_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)

-- Table: performance.mf_rating

-- DROP TABLE performance.mf_rating;

CREATE TABLE performance.mf_rating
(
    eff_dt date,
    fund_id character varying(30) COLLATE pg_catalog."default",
    rating numeric(20, 10),
    CONSTRAINT mf_rating_fund_fk FOREIGN KEY (fund_id)
        REFERENCES performance.mutual_fund (fund_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE,
    CONSTRAINT mf_return_fund_fk FOREIGN KEY (fund_id)
        REFERENCES performance.mutual_fund (fund_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE CASCADE
)

-- Table: performance.mf_return

-- DROP TABLE performance.mf_return;

CREATE TABLE performance.mf_return
(
    eff_dt date,
    fund_id character varying(30) COLLATE pg_catalog."default",
    daily_return numeric(40, 20),
    monthly_return numeric(40, 20),
    halfy_return numeric(40, 20),
    yearly_return numeric(40, 20)
)

-- Table: performance.mutual_fund

-- DROP TABLE performance.mutual_fund;

CREATE TABLE performance.mutual_fund
(
    fund_id character varying(30) COLLATE pg_catalog."default" NOT NULL,
    fund_name character varying(250) COLLATE pg_catalog."default",
    fund_manager character varying(100) COLLATE pg_catalog."default",
    CONSTRAINT mutual_fund_pk PRIMARY KEY (fund_id),
    CONSTRAINT fund_name_uk UNIQUE (fund_name)
)