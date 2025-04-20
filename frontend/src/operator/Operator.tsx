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
}

export interface OperatorData {
  operator?: {
    emotion?: EmotionAgent;
    action?: ActionAgent;
  };
}

export const Operator = () => {
  const { messages, content, setContent, socket, roles, webSocketData } =
    useWsChat<OperatorData>({
      role: "operator",
    });
  const { emotion = {}, action = {} } = webSocketData.operator || {};

  useEffect(() => {
    if (action.answer) {
      setContent(action.answer || "");
    }
  }, [action]);

  return (
    <Layout left={<Knowledge />} right={<Agents {...emotion} />}>
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
        <Flex justify="space-between" align="center">
          <Button type="default" className={styles.closeDialog}>
            Закончить диалог
          </Button>
          <Button type="primary" className={styles.newDialog}>
            Синтезировать новый диалог
          </Button>
        </Flex>
      </Flex>
    </Layout>
  );
};
