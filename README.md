# n.exchange backend evaluation

## Time Limit - 4 Hours
Please return your attempt of this task 4 hours from receiving it.

## Overview
This exercise is meant to test your coding skills as well as how you approach the development process in general. Your task is to take the provided state of the app, implement missing requirements and improve it for perfomance and high traffic. Also improve on your own expectation of code and app quality. How you choose to approach this task is up to you and you should make your own judgements about what’s most important to fix or implement first and take a best guess if unsure about something.

You should approach this app with the attitude that you and other developers may have to expand and maintain it for an unknown number of years and will likely outlive you working on it.

Since the time is limited, you are not expected to fix everything, so if you identify something as taking a long time to fix, just leave it.
If you identify some things you would like to do but run out of time for, feel free to submit some notes along with your task submission.

## Description of the app
Purpose of this app is to allow users to manage their crypto addresses. User can look up transactions and addresses from blockchain, track their own addresses statuses and manage incoming orders. Order is a transaction that address owner is expecting to receive to provide some service for agreed price.

All app functionality should be implemented as an API. Django admin panel is as a helper for developer and not expected as a requirement.

App functionality:
* Allows user to register and login via API
* Blockchain querying
	* User can search address or transaction of ETH, BTC or BCH and show the addresses/transactions that involve this specific transaction/address and their values
	* User can get list of his past searches
* User address management
	* User can mark an address as ‘mine’.
	* User can get the balance aggregated by currency from all the addresses he selected as mine
* User can manage crypto orders
	* User can create an order with specific amount and with response user will get order id and deposit address. Deposit address is picked from marked as mine addresses and each open order has different deposit wallet address. After order completion address can be reused.
	* User can mark order as complete through API.