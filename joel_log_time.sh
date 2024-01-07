#!/bin/bash


Help() {
   # Display help
   echo "🐢 Joel's Log Time"
   echo
   echo "Log your work time using this simple shell app."
   echo "Logged time data is stored in an sqlite database in this directory."
   echo
   echo "Syntax: scriptTemplate [-i|o|e|s]"
   echo "options:"
   echo "i     Date and time In (example: -i 2024-01-07T08:30)."
   echo "o     Date and time Out example: -o 2024-01-07T17:30."
   echo "e     End day by recording total work hours for the day."
   echo "s     Show saldo for all logged time entries."
   echo
}

In() {
   # Log In timestamp
   echo $1

   IFS="T"
   read -a datetime_split <<< $1
   echo "Date entered: ${datetime_split[0]}"
   echo "Time entered: ${datetime_split[1]}"
   unset IFS
}

Out() {
   # Log Out timestamp
   echo $1

   IFS="T"
   read -a datetime_split <<< $1
   echo "Date entered: ${datetime_split[0]}"
   echo "Time entered: ${datetime_split[1]}"
   unset IFS
}

Sum() {
   # Record total worked hours for the day
   echo "Sum"
}

Saldo() {
   # Show total saldo for all recorded days
   echo "Saldo"
}

ValidateDatetime() {
   # Validate date and time
   # Shorter version of ISO 8601 date (2004-02-12T15:19:21+00:00) -> 20023-11-05T08:30
   # Example: 2024-01-07T14:51
   datetime_valid=$(echo $1 | grep -E -w "^[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])T(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$")

   if [ -z $datetime_valid ];
   then
      echo "Invalid input datetime format: $1"
      echo "Valid format example: 2024-01-07T08:30"
      exit
   fi
}

ValidateDate() {
   # Validate date
   # Example: 2024-01-07
   date_valid=$(echo $1 | grep -E -w "^[0-9]{4}-(0[1-9]|1[0-2])-([0-2][0-9]|3[0-1])$")

   if [ -z $date_valid ];
   then
      echo "Invalid input date format: $1"
      echo "Valid format example: 2024-01-07"
      exit
   fi
}


# Show help if no args are given
if [ -z $1 ];
then
   Help
   exit
fi

while getopts "i:o:e:sh" option; do
   case $option in
      i)
         # Log an In time entry
         # Requires <date>
         # 2023-10-22T07:30
         ValidateDatetime $OPTARG
         In $OPTARG
         exit;;
      o)
         # Log an Out time entry
         # Requires <date>
         # 2023-10-22T07:30
         ValidateDatetime $OPTARG
         Out $OPTARG
         exit;;
      e)
         # End the day and sum all time entries
         # Requires <date>
         # 2023-10-22
         ValidateDate $OPTARG
         echo "sum"
         Sum
         exit;;
      s)
         # Show current saldo for all time entries
         echo "saldo"
         Saldo
         exit;;
      h)
         Help
         exit;;
      *)
         echo "Missing arguments or required argument value. Have a look at what's being served:"
         echo
         Help
         exit;;
   esac
done


# TODO:

# input date and/or time to epoch time
# https://stackoverflow.com/questions/10990949/convert-date-time-string-to-epoch-in-bash
date --date '18:00' +"%s"

# sqlite3 query for shell script
# https://sqlite.org/cli.html
sqlite3 test.db '.tables'
sqlite3 test.db 'select * from drinks'
#sqlite3 test.db 'create table drinks (id INTEGER);'

# diff epoch time between epoch timestamps

# sum many epoch timestamps