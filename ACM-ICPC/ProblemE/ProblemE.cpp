#include <iostream>
#include <vector>
#include <string>

using namespace std;

string convert_base_n(long int base_10, long int new_base);

int main()
{
    long int base_10_age;
    long int min_age;    
    string result;
    
    cin >> base_10_age >> min_age;
    
    for (long int cur_base = base_10_age; cur_base > 0; cur_base--)
    {
        try
        {
            result = convert_base_n(base_10_age, cur_base);
            if(stoi(result) >= min_age)
            {
                cout << cur_base << endl;
                break;
            }
        }
        catch(out_of_range){}
    }
}

string convert_base_n(long int base_10, long int new_base)
{
    string result = "";
    long int whole;
    long int remainder;
    long int temp = base_10;
    do
    {

        whole = temp/new_base;
        remainder = temp % new_base;
        
        if(remainder >= 10)
        {
            throw out_of_range("bit too high");
        }
        else
        {
            result.insert(0, to_string(remainder));
            temp = whole;
        }
    }while(whole != 0);
        
    return result;
}

