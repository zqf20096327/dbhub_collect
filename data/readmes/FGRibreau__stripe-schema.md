# [Stripe](http://stripe.com/) Schema

> For learning and inspiration, enjoy :+1:

 [![Slack](https://img.shields.io/badge/Slack-Join%20our%20tech%20community-17202A?logo=slack)](https://join.slack.com/t/fgribreau/shared_invite/zt-edpjwt2t-Zh39mDUMNQ0QOr9qOj~jrg)

* [accounts](#accounts)
* [accounts_metadata](#accounts_metadata)
* [external_account_bank_accounts](#external_account_bank_accounts)
* [external_account_cards](#external_account_cards)
* [application_fees](#application_fees)
* [balance_transactions](#balance_transactions)
* [balance_transaction_fee_details](#balance_transaction_fee_details)
* [charges](#charges)
* [charges_metadata](#charges_metadata)
* [coupons](#coupons)
* [coupons_metadata](#coupons_metadata)
* [credit_notes](#credit_notes)
* [credit_notes_metadata](#credit_notes_metadata)
* [credit_note_line_items](#credit_note_line_items)
* [credit_note_line_item_tax_amounts](#credit_note_line_item_tax_amounts)
* [customers](#customers)
* [customers_metadata](#customers_metadata)
* [disputes](#disputes)
* [disputes_metadata](#disputes_metadata)
* [early_fraud_warnings](#early_fraud_warnings)
* [application_fee_refunds](#application_fee_refunds)
* [application_fee_refunds_metadata](#application_fee_refunds_metadata)
* [invoices](#invoices)
* [invoices_metadata](#invoices_metadata)
* [invoice_line_items](#invoice_line_items)
* [invoice_items](#invoice_items)
* [invoice_items_metadata](#invoice_items_metadata)
* [transfers](#transfers)
* [transfers_metadata](#transfers_metadata)
* [plans](#plans)
* [plans_metadata](#plans_metadata)
* [products](#products)
* [products_metadata](#products_metadata)
* [refunds](#refunds)
* [refunds_metadata](#refunds_metadata)
* [sources](#sources)
* [sources_metadata](#sources_metadata)
* [subscriptions](#subscriptions)
* [subscriptions_metadata](#subscriptions_metadata)
* [subscription_items](#subscription_items)
* [tax_rates](#tax_rates)
* [tax_rates_metadata](#tax_rates_metadata)
* [transfer_reversals](#transfer_reversals)
* [transfer_reversals_metadata](#transfer_reversals_metadata)
* [usage_records](#usage_records)

## accounts

| attribute                                       | type      | comment                                                                                                                                                                                                                                                                                                                                 |
| ----------------------------------------------- | --------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| id                                              | varchar   | Unique identifier for the object.                                                                                                                                                                                                                                                                                                       |
| business_name                                   | varchar   |                                                                                                                                                                                                                                                                                                                                         |
| business_url                                    | varchar   |                                                                                                                                                                                                                                                      

[...截断...]

                                                                                   |
| country                                         | varchar   | The account's country.                                                                                                                                                                                                                                                                                                                  |
| created                                         | timestamp | Time at which the object was created. Measured in seconds since the Unix epoch.                                                                                                                                                                                                                                                         |
| debit_negative_balances                         | boolean   |                                                                                                                                                                                                                                                                                                                                         |
| default_currency                                | varchar   | Three-letter ISO currency code representing the default currency for the account. This must be a currency that [Stripe supports in the account's country](https://stripe.com/docs/payouts).                                                                                                                                             |
| details_submitted                               | boolean   | Whether account details have been submitted. Standard accounts cannot receive payouts before this is true.                                                                                                                                                                                                                              |
| display_name                                    | varchar   |                                                                                                                                                                                                                                                                                                                                         |
| email                                           | varchar   | The primary user's email address.                                                                                                                                                                                                                                                                                                       |
| payout_statement_descriptor                     | varchar   |                                                                                                                                                                                                                                                                                                                                         |
| payouts_enabled                                 | boolean   | Whether Stripe can send payouts to this account.                                                                                                                                                                                                                                                                                        |
| charges_enabled                                 | boolean   | Whether the account can create live charges.                                                                                                                                                                                                                                                                     