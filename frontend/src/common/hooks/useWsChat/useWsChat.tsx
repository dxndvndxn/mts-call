import { useEffect, useState } from "react";
import type { BubbleDataType } from "@ant-design/x/es/bubble/BubbleList";
import type { GetProp } from "antd";
import { Bubble } from "@ant-design/x";
import { UserOutlined } from "@ant-design/icons";

type UserType = "user" | "operator";

type WsResponse = {
  role?: string;
  content?: string;
  clearDialog?: boolean;
};

interface UseWsChatProps {
  role: UserType;
}

const roles: GetProp<typeof Bubble.List, "roles"> = {
  user: {
    placement: "start",
    avatar: { icon: <UserOutlined />, style: { background: "#fde3cf" } },
    typing: { step: 5, interval: 20 },
    style: {
      maxWidth: 600,
    },
  },
  operator: {
    placement: "end",
    avatar: { icon: <UserOutlined />, style: { background: "#87d068" } },
  },
};

export const useWsChat = <T,>({ role }: UseWsChatProps) => {
  const [content, setContent] = useState("");
  const [socket, setSocket] = useState<WebSocket>();
  const [webSocketData, setWebSocketData] = useState<T>({} as T);
  const [messages, setMessages] = useState<BubbleDataType[]>([]);

  useEffect(() => {
    const newChat = new WebSocket(
      `ws://${process.env.REACT_APP_API_BASE_URL}/ws/chat/${role}`,
    );

    newChat.onopen = () => {
      setSocket(newChat);
    };

    newChat.onmessage = (event) => {
      if (event.data) {
        const { role, content, clearDialog, ...restData } =
          (JSON.parse(event.data) as WsResponse) || {};

        if (clearDialog) {
          setWebSocketData({} as T);
          setContent("");
          setMessages([]);
          return;
        }

        if (role && content) {
          setMessages((messages) => {
            return [
              ...messages,
              {
                role,
                content,
              },
            ];
          });
        }
        setWebSocketData((currentData) => {
          return {
            ...currentData,
            ...restData,
          };
        });
      }
    };

    newChat.onclose = (event) => {
      console.log("onclose", event);
    };

    newChat.onerror = (error) => {
      console.error("onerror", error);
    };
  }, []);

  return {
    messages,
    content,
    setContent,
    setMessages,
    socket,
    roles,
    webSocketData,
    setWebSocketData,
  };
};
