import { XProvider } from "@ant-design/x";
import { theme } from "antd";
import { useOutlet } from "react-router";

import "./App.scss";

export const App = () => {
  const outlet = useOutlet();

  return (
    <XProvider
      theme={{
        algorithm: theme.darkAlgorithm,
        token: {
          colorPrimary: "#48494C",
        },
        components: {
          Layout: {
            bodyBg: "#1F2022",
          },
          Card: {
            headerBg: "#2E3033",
            colorBgContainer: "#1B1B1E",
            colorText: "#BFBFBF",
            colorTextHeading: "#FCFCFC",
            headerFontSizeSM: 16,
            headerPaddingSM: 24,
            bodyPaddingSM: 18,
            headerHeightSM: 51,
          },
        },
      }}
    >
      {outlet}
    </XProvider>
  );
};
