{
    "name": "My workflow",
    "nodes": [
        {
            "parameters": {"updates": ["message"], "additionalFields": {}},
            "type": "n8n-nodes-base.telegramTrigger",
            "typeVersion": 1.2,
            "position": [0, 0],
            "id": "d60aa8e4-4ff1-4714-8c77-172bc2427eb2",
            "name": "Telegram Trigger",
            "webhookId": "6f64f4a3-5aaa-447e-8630-0dee280df590",
            "credentials": {
                "telegramApi": {"id": "m0gt2jM2NakFhVcF", "name": "Telegram account"}
            },
        },
        {
            "parameters": {
                "rules": {
                    "values": [
                        {
                            "conditions": {
                                "options": {
                                    "caseSensitive": true,
                                    "leftValue": "",
                                    "typeValidation": "strict",
                                    "version": 2,
                                },
                                "conditions": [
                                    {
                                        "leftValue": "={{ $json.message.text }}",
                                        "rightValue": "/start",
                                        "operator": {
                                            "type": "string",
                                            "operation": "equals",
                                        },
                                        "id": "02f27878-4243-4c33-8cb0-fbd346915ae1",
                                    }
                                ],
                                "combinator": "and",
                            }
                        },
                        {
                            "conditions": {
                                "options": {
                                    "caseSensitive": true,
                                    "leftValue": "",
                                    "typeValidation": "strict",
                                    "version": 2,
                                },
                                "conditions": [
                                    {
                                        "id": "864292b0-0577-4241-8117-039b13493ad3",
                                        "leftValue": "={{ $json.message.text }}",
                                        "rightValue": "/help",
                                        "operator": {
                                            "type": "string",
                                            "operation": "equals",
                                            "name": "filter.operator.equals",
                                        },
                                    }
                                ],
                                "combinator": "and",
                            },
                            "renameOutput": true,
                            "outputKey": "Help",
                        },
                        {
                            "conditions": {
                                "options": {
                                    "caseSensitive": true,
                                    "leftValue": "",
                                    "typeValidation": "strict",
                                    "version": 2,
                                },
                                "conditions": [
                                    {
                                        "id": "f445d0a6-c619-4979-820b-a6ca35c6ad71",
                                        "leftValue": "={{ $json.message.text }}",
                                        "rightValue": "/reset",
                                        "operator": {
                                            "type": "string",
                                            "operation": "equals",
                                        },
                                    }
                                ],
                                "combinator": "and",
                            }
                        },
                        {
                            "conditions": {
                                "options": {
                                    "caseSensitive": true,
                                    "leftValue": "",
                                    "typeValidation": "strict",
                                    "version": 2,
                                },
                                "conditions": [
                                    {
                                        "id": "84a0f816-af1a-4217-b7d2-fbdb5a8e6ee7",
                                        "leftValue": "={{ $json.message.text }}",
                                        "rightValue": "/reset",
                                        "operator": {
                                            "type": "string",
                                            "operation": "exists",
                                            "singleValue": true,
                                        },
                                    }
                                ],
                                "combinator": "and",
                            }
                        },
                    ]
                },
                "options": {},
            },
            "type": "n8n-nodes-base.switch",
            "typeVersion": 3.3,
            "position": [208, 0],
            "id": "3587c5cb-1432-48cd-8e54-76e6cb2352b9",
            "name": "Switch",
        },
        {
            "parameters": {
                "method": "POST",
                "url": "={{ $env.API_BASE_URL }}/api/user/create",
                "sendBody": true,
                "specifyBody": "json",
                "jsonBody": '={\n  "tg_id": {{$json.message.from.id}},\n  "username": "{{$json.message.from.username}}",\n  "first_name": "{{$json.message.from.first_name}}",\n  "last_name": "{{$json.message.from.last_name}}",\n  "is_bot": {{$json.message.from.is_bot}},\n  "language_code": "{{$json.message.from.language_code}}"\n}',
                "options": {},
            },
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.3,
            "position": [432, -320],
            "id": "7951a78e-6181-41b5-b844-b0eb429e0c80",
            "name": "HTTP Request",
        },
        {
            "parameters": {
                "chatId": "={{ $json.message.chat.id }}",
                "text": "=Привет! Я бот с интеграцией ChatGPT. 🤖  Команды: /start - начать новый диалог (сбросить контекст) /help - показать эту справку  /reset - очистить историю сообщений Просто отправьте мне текстовое сообщение, и я отвечу используя ChatGPT с учётом контекста последних 10 сообщений.",
                "additionalFields": {"appendAttribution": false},
            },
            "type": "n8n-nodes-base.telegram",
            "typeVersion": 1.2,
            "position": [432, -128],
            "id": "6b2ca7eb-a7f2-4032-81ce-84393fc8689a",
            "name": "Send a text message",
            "webhookId": "43ba419b-2699-42eb-8f62-2dcd56b5dacd",
            "credentials": {
                "telegramApi": {"id": "m0gt2jM2NakFhVcF", "name": "Telegram account"}
            },
        },
        {
            "parameters": {
                "method": "POST",
                "url": "={{ $env.API_BASE_URL }}/api/dialogs/message",
                "sendBody": true,
                "specifyBody": "json",
                "jsonBody": '={\n  "content": "{{ $json.message.text }}",\n  "role": "user",\n  "tg_id": "{{ $json.message.from.id }}"\n}',
                "options": {},
            },
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.3,
            "position": [432, 240],
            "id": "cfda7018-c423-459b-ae4e-07e383a1631c",
            "name": "HTTP Request1",
        },
        {
            "parameters": {
                "method": "POST",
                "url": "={{ $env.API_BASE_URL }}/api/dialogs/reset",
                "sendBody": true,
                "specifyBody": "json",
                "jsonBody": '={\n  "tg_id": "{{ $(\'Telegram Trigger\').item.json.message.from.id }}"\n}',
                "options": {},
            },
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.3,
            "position": [432, 48],
            "id": "c09c7b11-d24d-4e0d-9a87-e769f2d99ea1",
            "name": "HTTP Request2",
        },
        {
            "parameters": {
                "url": "={{ $env.API_BASE_URL }}/api/dialogs/{{ $('Telegram Trigger').item.json.message.from.id }}/history",
                "sendQuery": true,
                "specifyQuery": "json",
                "jsonQuery": '{\n  "limit": 10\n}',
                "options": {},
            },
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.3,
            "position": [640, 240],
            "id": "a24a573c-c209-459d-a34e-353962917fc3",
            "name": "HTTP Request3",
        },
        {
            "parameters": {
                "method": "POST",
                "url": "https://llm.api.cloud.yandex.net/foundationModels/v1/completion",
                "sendHeaders": true,
                "headerParameters": {
                    "parameters": [
                        {
                            "name": "Authorization",
                            "value": "=Api-Key {{ $env.YANDEX_GPT_KEY }}",
                        },
                        {"name": "Content-Type", "value": "application/json"},
                    ]
                },
                "sendBody": true,
                "contentType": "=json",
                "specifyBody": "json",
                "bodyParameters": {"parameters": [{}]},
                "jsonBody": "={{ $json }}",
                "options": {},
            },
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.3,
            "position": [960, 240],
            "id": "5acef8cb-5fbe-43bd-af25-d82e0986f671",
            "name": "HTTP Request4",
        },
        {
            "parameters": {
                "jsCode": 'const catalog = $env.YANDEX_GPT_CATALOG || "b1gf1i21qjabctqt3r5v";\n\n// Получить историю из предыдущего узла\nconst history = $input.first().json.messages || [];\n\n// Преобразовать content → text для YandexGPT\nconst messages = history.map(msg => ({\n  role: msg.role,\n  text: msg.content\n}));\n\n// Добавить текущее сообщение пользователя из Telegram Trigger\nconst currentMessage = $(\'Telegram Trigger\').item.json.message.text;\nmessages.push({\n  role: "user",\n  text: currentMessage\n});\n\nreturn {\n  json: {\n    modelUri: `gpt://${catalog}/yandexgpt-lite/latest`,\n    completionOptions: {\n      stream: false,\n      temperature: 0.6,\n      maxTokens: 2000\n    },\n    messages: messages\n  }\n};'
            },
            "type": "n8n-nodes-base.code",
            "typeVersion": 2,
            "position": [800, 240],
            "id": "2c050d56-be24-4868-a4ce-4361ad268f9c",
            "name": "Code in JavaScript",
        },
        {
            "parameters": {
                "method": "POST",
                "url": "={{ $env.API_BASE_URL }}/api/dialogs/message",
                "sendBody": true,
                "specifyBody": "json",
                "jsonBody": '={\n  "content": "{{ $(\'Telegram Trigger\').item.json.message.text }}",\n  "role": "assistant",\n  "tg_id": "{{ $(\'Telegram Trigger\').item.json.message.from.id }}"\n}',
                "options": {},
            },
            "type": "n8n-nodes-base.httpRequest",
            "typeVersion": 4.3,
            "position": [1168, 240],
            "id": "7dc3162b-a1fb-43dc-b23c-cffa1671e243",
            "name": "HTTP Request5",
        },
        {
            "parameters": {
                "chatId": "={{ $('Telegram Trigger').item.json.message.chat.id }}",
                "text": "={{ $('HTTP Request4').item.json.result.alternatives[0].message.text }}",
                "additionalFields": {"appendAttribution": false},
            },
            "type": "n8n-nodes-base.telegram",
            "typeVersion": 1.2,
            "position": [1376, 240],
            "id": "1df7d9ff-e184-470f-87c8-f3c2a75f54c2",
            "name": "Send a text message1",
            "webhookId": "dc53aed6-4f33-4e29-9dda-aa0aa8fa0279",
            "credentials": {
                "telegramApi": {"id": "m0gt2jM2NakFhVcF", "name": "Telegram account"}
            },
        },
    ],
    "pinData": {},
    "connections": {
        "Telegram Trigger": {
            "main": [[{"node": "Switch", "type": "main", "index": 0}]]
        },
        "Switch": {
            "main": [
                [{"node": "HTTP Request", "type": "main", "index": 0}],
                [{"node": "Send a text message", "type": "main", "index": 0}],
                [{"node": "HTTP Request2", "type": "main", "index": 0}],
                [{"node": "HTTP Request1", "type": "main", "index": 0}],
            ]
        },
        "HTTP Request": {"main": [[]]},
        "Send a text message": {"main": [[]]},
        "HTTP Request1": {
            "main": [[{"node": "HTTP Request3", "type": "main", "index": 0}]]
        },
        "HTTP Request3": {
            "main": [[{"node": "Code in JavaScript", "type": "main", "index": 0}]]
        },
        "Code in JavaScript": {
            "main": [[{"node": "HTTP Request4", "type": "main", "index": 0}]]
        },
        "HTTP Request4": {
            "main": [[{"node": "HTTP Request5", "type": "main", "index": 0}]]
        },
        "HTTP Request5": {
            "main": [[{"node": "Send a text message1", "type": "main", "index": 0}]]
        },
    },
    "active": false,
    "settings": {"executionOrder": "v1"},
    "versionId": "f320f75a-12c6-4085-a25e-db9cb20662ad",
    "meta": {
        "templateCredsSetupCompleted": true,
        "instanceId": "383285ac420258bb2f665217997d4abc17e646e7d9a21227f72e0cde315d9fad",
    },
    "id": "YYUQjKTHTfb34FFf",
    "tags": [],
}
