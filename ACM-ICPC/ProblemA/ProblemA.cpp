#include <iostream>
#include <vector>

using namespace std;
bool balanced(vector<float> ideal_fractions, int sweets_eaten[]);

int main()
{
    int num_sweet_types;
    int num_sweets_eaten;
    int temp;  
    int total_sweets=0;
    
    cin >> num_sweet_types >> num_sweets_eaten;
    
    int sweets_eaten[num_sweet_types] = { };
    int proportions[num_sweet_types] = { };
    float ideal_fractions[num_sweet_types] = { };
    int sweets_eaten_sequence[num_sweet_types] = { };
    
    for(int i = 0; i< num_sweet_types; i++)
    {
        cin >> temp;
        total_sweets += temp;
        proportions[i] = temp;
    }
    
    for(int i = 0; i< num_sweets_eaten; i++)
    {
        cin >> temp;
        sweets_eaten[temp-1]++;
    }
    
    for(int i = 0; i< num_sweet_types; i++)
    {   
        ideal_fractions[i] = (float)proportions[i]/(float)total_sweets;
    }
}

bool balanced(vector<float> ideal_fractions, int sweets_eaten[])
{

}
