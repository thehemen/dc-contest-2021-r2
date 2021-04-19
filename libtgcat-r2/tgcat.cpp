#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <fstream>

#include "fasttext/fasttext.h"
#include "nlohmann/json.hpp"

#include "tgcat.h"
#include "utils.h"
#include "lang_detect.h"

using namespace std;
using json = nlohmann::json;

map<string, double> settings;
fasttext::FastText langFastText;

int tgcat_init()
{
    ifstream i("resources/settings.json");
    json j;
    i >> j;

    for(const auto & [key, val] : j.items())
    {
        settings[key] = val;
    }

    langFastText.loadModel("resources/lid.176.bin");
    return 0;
}

int tgcat_detect_language(const struct TelegramChannelInfo *channel_info, char language_code[6])
{
    setlocale(LC_ALL, "");

    TelegramChannel telegramChannel(channel_info);
    pair<string, double> lang_score = detect_language(langFastText, settings, telegramChannel.full_text);
    memcpy(language_code, lang_score.first.c_str(), lang_score.first.size() + 1);
    return 0;
}

int tgcat_detect_category(const struct TelegramChannelInfo *channel_info, double category_probability[TGCAT_CATEGORY_OTHER + 1])
{
    (void)channel_info;
    memset(category_probability, 0, sizeof(double) * (TGCAT_CATEGORY_OTHER + 1));

    int i;

    for (i = 0; i < 10; i++)
    {
        category_probability[rand() % (TGCAT_CATEGORY_OTHER + 1)] += 0.1;
    }

    return 0;
}
