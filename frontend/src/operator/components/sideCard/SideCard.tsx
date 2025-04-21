import React from "react";
import { Card, Button, Flex } from "antd";
import { ArrowUpOutlined } from "@ant-design/icons";
import styles from "./SideCard.module.scss";

interface SideCardProps {
  title: string;
  text?: string | React.JSX.Element;
  action?: () => void;
}

export const SideCard = ({ title, action, text }: SideCardProps) => {
  return (
    <Card
      title={
        <Flex justify="space-between" align="center">
          <span>{title} </span>
          {action && (
            <Button className={styles.action}>
              <ArrowUpOutlined />
            </Button>
          )}
        </Flex>
      }
      size="small"
    >
      <p>{text}</p>
    </Card>
  );
};
