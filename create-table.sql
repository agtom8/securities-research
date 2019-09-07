USE Securities;
CREATE SCHEMA Finyahoo;
GO
CREATE TABLE Finyahoo.Secprice
(
	insert_date DATE NOT NULL DEFAULT (CONVERT(DATE, CURRENT_TIMESTAMP)),
	symbol NVARCHAR(8) NOT NULL,
	cur_price MONEY NOT NULL,
	prev_close MONEY NULL DEFAULT (0),
	day_open MONEY NULL,
	bid MONEY NULL,
	bid_qty INT NULL,
	ask MONEY NULL,
	ask_qty INT NULL,
	day_min MONEY NULL,
	day_max MONEY NULL,
	ftw_min MONEY NULL,                   -- 52 week min
	ftw_max MONEY NULL,                   -- 52 week max
	day_vol INT NULL,                     -- day volume
	avg_vol INT NULL,                     -- avg volume
	mkt_cap VARCHAR(15) NULL,                 -- current market capitalization
	pe_ratio VARCHAR(10) NULL,                -- price/earnings ratio
	eps VARCHAR(10) NULL,                     -- earnings per share - may or may not be applicable
	fwd_div_yld VARCHAR(15) NULL,             -- forward dividend yield
	exdiv_date VARCHAR(10) NULL,              -- ex-dividend date
	one_year_tgt_est VARCHAR(10) NULL         -- 1 year target estimate
	CONSTRAINT PK_Secprice PRIMARY KEY (symbol, insert_date),
	CONSTRAINT UQ_Secprice UNIQUE (insert_date, symbol)
);
GO