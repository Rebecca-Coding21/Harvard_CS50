-- Keep a log of any SQL queries you execute as you solve the mystery.
--get all description of crimes at that date in that street
SELECT description FROM crime_scene_reports WHERE year = "2021" AND month = "7" AND day = "28" AND street = "Humphrey Street";

--get inteviews from witnesses to get more information about the theft
SELECT name, transcript FROM interviews
WHERE year = "2021" AND month = "7" AND day = "28";

--get possible account numbers of thief
SELECT account_number, amount FROM atm_transactions
WHERE year = "2021" AND month = "7" AND day = "28" AND atm_location = "Leggett Street" AND transaction_type = "withdraw";

--get possible license_plte of thief for time around 10;25 am and owner name
SELECT name, phone_number, passport_number, license_plate FROM people
WHERE license_plate IN(SELECT license_plate FROM bakery_security_logs WHERE year = "2021" AND month = "7" AND day = "28" AND hour = "10" AND (minute between "15" AND "25") AND activity = "exit");
--Vanessa, Barry, Iman, Sofia, Luca, Diara, Kelsey,Bruce

--get name of people who withdrawed at atm and find matching names with previous query
SELECT name, bank_accounts.account_number FROM people, atm_transactions, bank_accounts
WHERE people.id = bank_accounts.person_id AND year = "2021" AND month = "7" AND day = "28" AND atm_transactions.account_number = bank_accounts.account_number AND atm_location = "Leggett Street" AND transaction_type = "withdraw";
--Bruce, DIara, Iman, Luca (Matching with people from parking lot)

--find matches between phone calls at that day
SELECT caller, name FROM phone_calls, people
WHERE people.phone_number = caller AND year = "2021" AND month = "7" AND day = "28" AND duration <60;
--Bruce, Diara

--Find out what was the earliest flight the next day and if Bruce or Diara where on it.
SELECT full_name, city, hour, minute, people.name, people.passport_number FROM flights, airports, people, passengers
WHERE flights.id = passengers.flight_id AND passengers.passport_number = people.passport_number AND year = "2021" AND month = "7" AND day = "29" AND airports.id = flights.destination_airport_id
AND flights.origin_airport_id= (SELECT airports.id FROM airports WHERE city = "Fiftyville")
ORDER BY flights.hour;
--Bruce is only one on flight to New York (= earliest)

--find out who Bruce was calling
SELECT receiver, name FROM phone_calls, people
WHERE people.phone_number = receiver AND year = "2021" AND month = "7" AND day = "28" AND duration <60 AND phone_calls.caller IN(SELECT phone_number FROm people WHERE name = "Bruce");
--Robin = acomplice
