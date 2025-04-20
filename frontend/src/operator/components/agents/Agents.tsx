import { Space } from "antd";
import { SideCard } from "../sideCard";
import { EmotionAgent } from "../../Operator";

export const Agents = ({ emotion }: EmotionAgent) => {
  const emotionText = emotion ? `Эмоция ${emotion}` : "";

  return (
    <Space direction="vertical" size="large">
      <SideCard
        title="Эмоциональное состояние клиента"
        text={`${emotionText}`}
      />
      <SideCard title="Контроль стандартов общения" action={() => ({})} />
      <SideCard title="Заполнение  CRM" action={() => ({})} />
    </Space>
  );
};
