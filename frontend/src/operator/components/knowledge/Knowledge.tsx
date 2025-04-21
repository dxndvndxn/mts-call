import { Card } from "antd";

interface KnowledgeProps {
  text?: string;
}

export const Knowledge = ({ text }: KnowledgeProps) => {
  return (
    <Card title="База знаний" size="small">
      {text || ""}
    </Card>
  );
};
