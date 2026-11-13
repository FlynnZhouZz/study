
配置项：
```js
export const google = {
    translateApiUrl:
        'https://translation.googleapis.com/language/translate/v2',
    // Flynn 谷歌账号api key （有免费额度（通常每月500,000字符））
    translateApiKey: 'xxxx',
};
```


工具
```js
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { google } from '@/config';

export async function translateText(
    text: string,
    target: string,
    source = 'en',
): Promise<string> {
    if (!google.translateApiKey) return text;
    try {
        const res = await fetch(
            `${google.translateApiUrl}?key=${google.translateApiKey}`,
            {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    q: text,
                    source,
                    target,
                    format: 'text',
                }),
            },
        );
        const data = await res.json();
        // Google Translate 超额时返回 403，或 error.code === 403
        if (
            data?.error?.code === 403 ||
            data?.error?.status === 'PERMISSION_DENIED' ||
            data?.error?.message?.includes('exceeded')
        ) {
            // 额度超限，直接降级为原文
            return text;
        }
        if (data?.data?.translations?.[0]?.translatedText) {
            return data.data.translations[0].translatedText;
        }
        return text;
    } catch {
        // 网络或API不可用时，直接返回原文
        return text;
    }
}

// 通用 React Hook，自动根据当前语言翻译文本
export function useTranslatedText(text: string, source = 'en') {
    const { i18n } = useTranslation();
    const [translated, setTranslated] = useState(text);

    useEffect(() => {
        let cancelled = false;
        async function doTranslate() {
            // 只翻译非英文，且有API KEY
            if (i18n.language !== source && google.translateApiKey) {
                const result = await translateText(text, i18n.language, source);
                if (!cancelled) setTranslated(result);
            } else {
                setTranslated(text);
            }
        }
        doTranslate();
        return () => {
            cancelled = true;
        };
    }, [text, i18n.language, source]);

    return translated;
}
```