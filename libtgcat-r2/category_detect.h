#include <vector>
#include <locale>
#include <cctype>
#include <codecvt>
#include <algorithm>
#include <fstream>
#include <sstream>

#include "fasttext/fasttext.h"

#ifndef CATEGORY_DETECT_H
#define CATEGORY_DETECT_H

using namespace std;

vector<string> get_category_list(const char* filename)
{
    vector<string> categories;
    ifstream infile(filename);
    string category;

    while(getline(infile, category))
    {
    	// Make FastText format like "__label__Art_&_Design".
    	replace_if(category.begin(), category.end(), [] (const char& c) { return c == ' ';}, '_');
        ostringstream ostream;
        ostream << "__label__";
        ostream << category;
        category = ostream.str();
        categories.push_back(category);
    }

    return categories;
}

bool is_char_good(wchar_t c, vector<pair<wchar_t, wchar_t>> ranges)
{
    if(c == L' ')
    {
        return true;
    }
    else
    {
        bool flag = false;

        for(const auto& [first, second]: ranges)
        {
            if(c >= first && c <= second)
            {
                flag = true;
                break;
            }
        }

        return flag;
    }
}

bool BothAreSpaces(wchar_t lhs, wchar_t rhs) { return (lhs == rhs) && (lhs == L' '); }

wstring remove_non_alpha(wstring s, vector<pair<wchar_t, wchar_t>> ranges)
{
    //Make alphabetic characterw to lower
    transform(s.begin(), s.end(), s.begin(), ::towlower);

    //Replace non-alphabetic characters with spaces
    std::replace_if(s.begin(), s.end(), [ranges](auto const& c) -> bool
    { 
        return !is_char_good(c, ranges);
    }, L' ');

    //Remove duplicate spaces
    s.erase(unique(s.begin(), s.end(), BothAreSpaces), s.end());

    //Remove leading spaces
    s.erase(s.begin(), find_if(s.begin(), s.end(), bind1st(not_equal_to<wchar_t>(), L' ')));

    //Remove trailing spaces
    s.erase(find_if(s.rbegin(), s.rend(), bind1st(not_equal_to<wchar_t>(), L' ')).base(), s.end());
    return s;
}

vector<double> get_category_probabilities(fasttext::FastText& fastText, vector<string> categories, wstring text)
{
	const int32_t k = 50;  // The number of categories.
	vector<double> probabilities(k);

	string utf8_text = wstring_to_utf8(text);
    istringstream utf8_stream(utf8_text);

    vector<pair<fasttext::real, string>> predictions;
    fastText.predictLine(utf8_stream, predictions, k, 0.0);

    for(int i = 0, len = predictions.size(); i < len; ++i)
    {
    	auto it = find(categories.begin(), categories.end(), predictions[i].second);

    	if(it != categories.end())
    	{
    		int category_index = it - categories.begin();
    		probabilities[category_index] = predictions[i].first;
    	}
    }

	return probabilities;
}

#endif