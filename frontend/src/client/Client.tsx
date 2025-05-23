import { Layout } from "../layout";
import { Flex } from "antd";
import { Bubble, Sender } from "@ant-design/x";
import { useWsChat } from "../common/hooks";

import styles from "./Client.module.scss";
const role = "user";

export const Client = () => {
  const { socket, roles, content, setContent, messages, setMessages } =
    useWsChat({
      role,
    });

  return (
    <Layout>
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
      </Flex>
    </Layout>
  );
};
