#include <bits/stdc++.h>
using namespace std;

int days_in_months[] = {0,31,29,31,30,31,30,31,31,30,31,30,31};

void check(bool valid)
{
    if(valid) return;

	cout <<"Invalid Date";
	exit(0);
}

bool is_leap_year(int year)
{
	if(year % 400 == 0) return true;
	else if(year % 100 == 0) return false;
	else if(year % 4 == 0) return true;
	else return false;
}

void print(int day,int month,int year)
{
	if(day <= 9) cout << '0';
	cout << day;
	cout << '-';
	
	if(month <= 9) cout << '0';
	cout << month;
	cout << '-';
	
	cout << year;

	exit(0);
}

int main()
{
    string date;
    
	//check if input string is given or not 
    if(cin >> date) ;
    else check(0);
        
    char c;
    if(!(cin >> c)) ;
    else check(0); //check that no further data is given apart from one string
    
    check(date.length() == 10); //DD-MM-YYYY format has 10 letters
    
    //Check the positions of - and numbers
    for(int i=0;i<10;i++)
        if(i == 2 || i == 5) check(date[i] == '-');
        else check(date[i] >= '0' && date[i] <= '9');
        
    int day = (date[0] - '0')*10 + (date[1] - '0');
	int month = (date[3] - '0')*10 + (date[4] - '0');
	int year = (date[6] - '0')*1000 + (date[7] - '0')*100 + (date[8] - '0')*10 + (date[9] - '0');

	//Check for validity of date
	check(year >= 1900 && year <= 2015);

	check(month >= 1 && month <= 12);

	check(day >= 1 && day <= days_in_months[month]);
	if(is_leap_year(year)) check(day <= 28);

	//Now get the previous day
	if(day >= 2) day--;
	else if(month == 3)
	{
		month = 2;

		if(is_leap_year(year)) day = 29;
		else day = 28;
	}
	else if(month != 1)
	{
		month--;
		day = days_in_months[month];
	}
	else
	{
		year--;
		month = 12;
		day = 31;
	}

	print(day,month,year);
}