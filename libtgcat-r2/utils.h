#include <vector>
#include <locale>
#include <cctype>
#include <codecvt>

#include "tgcat.h"

#ifndef UTILS_H
#define UTILS_H

using namespace std;

wstring char_to_wstring(const char* s)
{
    wstring_convert<codecvt_utf8<wchar_t>, wchar_t> converter;
    return converter.from_bytes(s);
}

wstring utf8_to_wstring(const string& str)
{
    wstring_convert<codecvt_utf8<wchar_t>> myconv;
    return myconv.from_bytes(str);
}

string wstring_to_utf8(const wstring& str)
{
    wstring_convert<codecvt_utf8<wchar_t>> myconv;
    return myconv.to_bytes(str);
}

struct TelegramChannel
{
    wstring title;
    wstring description;
    vector<wstring> posts;

    wstring full_text;

    TelegramChannel(const struct TelegramChannelInfo *channel_info)
    {
        this->title = char_to_wstring(channel_info->title);
        this->description = char_to_wstring(channel_info->description);
        this->posts = vector<wstring>();

        for (size_t i = 0, recent_post_count = channel_info->recent_post_count; i < recent_post_count; i++)
        {
            TelegramChannelPost post = channel_info->recent_posts[i];
            this->posts.push_back(char_to_wstring(post.text));
        }

        this->full_text = get_full_text(this->title, this->description, this->posts);
    }

    wstring get_full_text(wstring title, wstring description, vector<wstring> posts)
    {
        wstring result;
        result += title + L"\n";
        result += description + L"\n";

        for (size_t i = 0, post_count = posts.size(); i < post_count; i++)
        {
            result += posts[i] + L"\n";
        }

        return result;
    }
};

#endif