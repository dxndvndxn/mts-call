import { Space } from "antd";
import { SideCard } from "../sideCard";
import { ActionAgent, EmotionAgent, SummaryAgent } from "../../Operator";

type AgentsProps = EmotionAgent & ActionAgent & SummaryAgent;

export const Agents = ({ emotion, quality, final, type }: AgentsProps) => {
  const emotionText = emotion ? `${emotion}` : "";
  const summary = (
    <>
      {type && (
        <>
          Типа обращения: {type}
          <br />
        </>
      )}
      {emotion && (
        <>
          Состояние клиента: {emotion}
          <br />
        </>
      )}
      {final && `Итог диалога: ${final}`}
    </>
  );

  return (
    <Space direction="vertical" size="large">
      <SideCard
        title="Эмоциональное состояние клиента"
        text={`${emotionText}`}
      />
      <SideCard title="Контроль стандартов общения" text={quality || ""} />
      <SideCard text={summary} title="Заполнение  CRM" action={() => ({})} />
    </Space>
  );
};
