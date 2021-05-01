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

wstring remove_non_alpha(wstring s)
{
    std::replace_if(s.begin(), s.end(), [](auto const& c) -> bool
    { 
        return !(std::iswalnum(c) && !std::iswdigit(c) || c == L' ');
    }, L' ');

    transform(s.begin(), s.end(), s.begin(), ::towlower);
    s.erase(unique(s.begin(), s.end()), s.end());
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