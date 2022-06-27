import React from "react";
import mainLogo from "./images/ikloa2.png";
import TerminalUI from "./Terminal";
import LoaderUI from "./Loading";

export default function Home() {
  const [terminal, setTerminal] = React.useState(false);
  const [loading, setLoading] = React.useState(false);

  const toggleLoader = () => {
    setLoading(!loading);
  };

  React.useEffect(() => {
    setTimeout(() => {
      setLoading(true);
    }, 1000);
    setTimeout(() => {
      setTerminal(true);
      setLoading(false);
    }, 3000);
  }, []);

  return (
    <div
      style={{
        backgroundImage: `url(${mainLogo})`,
        minHeight: "648px",
        backgroundRepeat: "no-repeat",
        backgroundPosition: "center",
        backgroundColor: "black",
        backgroundSize: "87% auto",
      }}
    >
      {loading ? <LoaderUI toggleLoader={toggleLoader} /> : null}
      {terminal ? (
        <div style={{ width: "100%" }}>
          <TerminalUI />{" "}
        </div>
      ) : null}
    </div>
  );
}
