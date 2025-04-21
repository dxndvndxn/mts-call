import { useEffect, useState } from "react";
import { useWsChat } from "../common/hooks";
import { Bubble, Sender } from "@ant-design/x";
import { Flex, Button } from "antd";
import { Layout } from "../layout";
import { Knowledge, Agents } from "./components";

import styles from "./Operator.module.scss";

export interface EmotionAgent {
  emotion?: string;
}

export interface ActionAgent {
  answer?: string;
  quality?: string;
}

export interface SummaryAgent {
  type?: string;
  final?: string;
}

export interface OperatorData {
  operator?: {
    emotion?: EmotionAgent;
    action?: ActionAgent;
    summary?: SummaryAgent;
    knowledge?: string;
  };
}

export const Operator = () => {
  const {
    messages,
    content,
    setContent,
    socket,
    roles,
    webSocketData,
    setWebSocketData,
    setMessages,
  } = useWsChat<OperatorData>({
    role: "operator",
  });
  const {
    emotion = {},
    action = {},
    knowledge,
    summary,
  } = webSocketData.operator || {};

  const clearDialog = () => {
    socket?.send("clearDialog");
  };

  useEffect(() => {
    if (action.answer) {
      setContent(action.answer || "");
    }
  }, [action]);

  return (
    <Layout
      left={<Knowledge text={knowledge} />}
      right={<Agents {...emotion} {...action} {...summary} />}
    >
      <Flex vertical gap="middle" className={styles.chat}>
        <Bubble.List roles={roles} items={messages} />
        <Sender
          footer={({ components }) => {
            const { ClearButton } = components;
            return <ClearButton />;
          }}
          value={content}
          onChange={setContent}
          onSubmit={(nextContent) => {
            socket?.send(nextContent);
            setContent("");
          }}
        />
        <Flex justify="end" align="center">
          <Button
            type="primary"
            className={styles.newDialog}
            onClick={clearDialog}
          >
            Закончить диалог
          </Button>
        </Flex>
      </Flex>
    </Layout>
  );
};
