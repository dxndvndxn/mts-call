import { ReactNode, PropsWithChildren } from "react";
import { Layout as AntdLayout, Space } from "antd";
import styles from "./Layout.module.scss";

const { Content } = AntdLayout;
const { Compact } = Space;

interface LayoutCallProps {
  left?: ReactNode;
  right?: ReactNode;
}

export const Layout = ({
  left,
  children,
  right,
}: PropsWithChildren<LayoutCallProps>) => {
  return (
    <AntdLayout className={styles.layout}>
      <Content className={styles.content}>
        <Space size="middle" direction="horizontal" align="end">
          {left && (
            <Compact direction="vertical" className={styles.side}>
              {left}
            </Compact>
          )}
          <Compact direction="vertical">{children}</Compact>
          {right && (
            <Compact direction="vertical" className={styles.side}>
              {right}
            </Compact>
          )}
        </Space>
      </Content>
    </AntdLayout>
  );
};
