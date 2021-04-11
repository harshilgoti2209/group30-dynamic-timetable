#include<bits/stdc++.h>
using namespace std;

mt19937 rng(chrono::steady_clock::now().time_since_epoch().count());

int getRand(int l, int r)
{
	uniform_int_distribution<int> uid(l, r);
	return uid(rng);
}

signed main()
{

#ifndef ONLINE_JUDGE
	freopen("input.txt", "r", stdin);
	freopen("output.txt", "w", stdout);
#endif

	vector<char> v;
	for (char ch = 'a'; ch <= 'z'; ch++)
	{
		v.push_back(ch);
	}
	for (char ch = 'A'; ch <= 'Z'; ch++)
	{
		v.push_back(ch);
	}
	for (char ch = '0'; ch <= '1'; ch++)
	{
		v.push_back(ch);
	}
	string s;
	while (cin >> s)
	{
		int rnd = getRand(0, 3);
		for (int i = 1; i <= rnd; i++)
		{
			int id = getRand(0, s.length() - 1);
			int pt = getRand(0, v.size() - 1);
			s[id] = v[pt];
		}
		cout << s << endl;
	}
	return 0;
}