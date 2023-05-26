-- lovefi app tables
-- updating a record replaces its older version, historical changes will be saved seperatly (i.e. daily extracts to a data warehouse)

-- users from lovefi app
-- 1 row per user
CREATE TABLE `users` (
	`id` varchar(255) NOT NULL PRIMARY KEY, -- id of the user from lovefi app, UNIQUE
	`name` varchar(255) NOT NULL, -- name of the user from lovefi app
    `email` varchar(255) NOT NULL, -- email adress of the user from lovefi app
    `phone` varchar(20), -- phone number of the user from lovefi app
    `_last_updated_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- items from Plaid, a connection between a user and its financial institution credentials saved by Plaid
-- 1 row per item + user UNIQUE
CREATE TABLE `item_connections` (
	`id` varchar(255) NOT NULL PRIMARY KEY, -- id of the item from Plaid
    `user_id` varchar(255) NOT NULL REFERENCES users(id), -- id of the user from lovefi app
	`access_token` varchar(255) NOT NULL, -- item access_token from Plaid to query Plaid API
    `institution_id` varchar(255) NOT NULL, -- id of the financial institution
    `institution_name` varchar(255) NOT NULL, -- name of the financial institution
    `_last_updated_at` timestamp DEFAULT CURRENT_TIMESTAMP
);

-- financial accounts from Plaid
-- 1 row per account + user UNIQUE
CREATE TABLE `accounts` (
    `id` varchar(255) NOT NULL PRIMARY KEY, -- id of the financial account from Plaid
    `user_id` varchar(255) NOT NULL REFERENCES users(id), -- id of the user from lovefi app
    `item_id` varchar(255) NOT NULL REFERENCES item_connections(id), -- id of the item from Plaid
    `people`json, -- array of ids of the users sharing this account from lovefi app
    `mask` char(4) NOT NULL, -- last digits of financial institution's account id from Plaid
    `official_name` varchar(255) NOT NULL, -- name of the financial account from Plaid
    `name` varchar(255) NOT NULL, -- alias of the financial account from Plaid
    `type` varchar(255), -- tyoe of the financial account from Plaid
    `subtype` varchar(255), -- subtyoe of the financial account from Plaid
    `iso_currency_code` char(3) NOT NULL, -- currency of the financial account from Plaid
    `balance_available` decimal(10,2) NOT NULL, -- spendable amount of the financial account from Plaid
    `balance_current` decimal(10,2) NOT NULL, -- current balance of the financial account from Plaid
    `_last_updated_at` timestamp DEFAULT CURRENT_TIMESTAMP
);

-- transactions from Plaid with additionnal parameter from lovefi app
-- id + account_id is UNIQUE
CREATE TABLE `transactions`(
    `id` varchar(255) NOT NULL PRIMARY KEY, -- id of the transaction from plaid
    `user_id` varchar(255) NOT NULL REFERENCES users(id), -- id of the user from lovefi app
    `item_id` varchar(255) NOT NULL REFERENCES item_connections(id), -- id of the item from Plaid
    `account_id` varchar(255) NOT NULL REFERENCES accounts(id), -- id of the financial account from Plaid
    `account_name` varchar(255) NOT NULL REFERENCES accounts(name), -- alias of the financial account from Plaid
    `plaid_category_id` varchar(255), -- id of the transaction category from Plaid
    `plaid_category` json, -- array? of the transaction category and subcategory from Plaid
    `date` date NOT NULL, -- date of the transaction from Plaid
    `authorized_date` date, -- date of the authorization of the transaction fron Plaid
    `name` varchar(255) NOT NULL, -- name of the transaction from Plaid
    `merchant_name` varchar(255), -- name of the merchant from Plaid
    `location` json, -- location of the merchant as key-value pairs from Plaid
    `payment_channel` varchar(255), -- channel of the payment from Plaid
    `iso_currency_code` char(3) NOT NULL, -- currency of the transaction from Plaid
    `amount` decimal(10,2) NOT NULL, -- amount of the transaction from Plaid
    `pending` boolean NOT NULL, -- pending flag of the transaction from Plaid
    `pending_transaction_id` varchar(255), -- id of the transaction as pending from Plaid
    `type` varchar(255), -- type of transaction from lovefi app
    `split_categories` json, -- categories and amounts of the transaction as key-value pairs from lovefi app
    `split_people` json, -- users and amounts of the transaction as key-value-pairs from lovefi app
    `tags` json, -- array of tags associatied with the transaction for advanced filtering such as 'WAITING FOR REFUND' or 'TO INVESTIGATE' from lovefi app
    `_last_updated_at` timestamp DEFAULT CURRENT_TIMESTAMP
);

-- categories of transactions from lovefi app
-- type + category + subcategory is UNIQUE
CREATE TABLE `categories`{
    `type` varchar(255), -- type of transactions from lovefi app
    `category` varchar(255), -- categories of transactions within transaction types
    `subcategory` varchar(255), -- subcategoriees of transactions within transaction category
    `user_id` varchar(255) NOT NULL REFERENCES users(id) -- id of the user from lovefi app
};

-- tags of transactions from lovefi app
-- tag + user is UNIQUE
CREATE TABLE `tags`{
    `id` int(50) NOT NULL PRIMARY KEY, -- id of the tag from lovefi app
    `name` varchar(255) NOT NULL, -- name of the tag from lovefi app
    `user_id` varchar(255) NOT NULL REFERENCES users(id) -- id of the user from lovefi app
};