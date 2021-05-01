#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fstream>

#include "fasttext/fasttext.h"
#include "nlohmann/json.hpp"

#include "tgcat.h"
#include "utils.h"

#include "lang_detect.h"
#include "category_detect.h"

using namespace std;
using json = nlohmann::json;

map<string, double> settings;
vector<string> categories;

fasttext::FastText lang_model;
map<string, fasttext::FastText> cat_models;

int tgcat_init()
{
    ifstream i("resources/settings.json");
    json j;
    i >> j;

    lang_model.loadModel(j["lang_model"]);
    categories = get_category_list(string(j["category_list"]).c_str());

    for(const auto & [key, val] : j["language"].items())
    {
        settings[key] = val;
    }

    for(const auto & [key, val] : j["category"].items())
    {
        cat_models[key].loadModel(val);
    }

    return 0;
}

int tgcat_detect_language(const struct TelegramChannelInfo *channel_info, char language_code[6])
{
    setlocale(LC_ALL, "");

    TelegramChannel telegramChannel(channel_info);
    pair<string, double> lang_score = detect_language(lang_model, settings, telegramChannel.full_text);
    memcpy(language_code, lang_score.first.c_str(), lang_score.first.size() + 1);
    return 0;
}

int tgcat_detect_category(const struct TelegramChannelInfo *channel_info, double category_probability[TGCAT_CATEGORY_OTHER + 1])
{
    TelegramChannel telegramChannel(channel_info);
    wstring text = telegramChannel.full_text;
    pair<string, double> lang_score = detect_language(lang_model, settings, text);

    vector<double> probabilities;
    string language = lang_score.first;

    if(cat_models.count(language) != 0)
    {
        wstring non_alpha_text = remove_non_alpha(text);
        probabilities = get_category_probabilities(cat_models[language], categories, non_alpha_text);
    }

    memset(category_probability, 0, sizeof(double) * (TGCAT_CATEGORY_OTHER + 1));

    for (int i = 0, len = probabilities.size(); i < len; i++)
    {
        category_probability[i] = probabilities[i];
    }

    return 0;
}