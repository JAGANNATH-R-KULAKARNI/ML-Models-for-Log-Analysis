import React from "react";
import axios from "axios";

export default function Shell() {
  const [data, setData] = React.useState([]);
  const [textc, setTextc] = React.useState("");
  const [prevCount, setPrevCount] = React.useState(0);
  const [updater, setUpdater] = React.useState(false);

  const help = (
    <div
      style={{
        color: "white",
        width: "100%",
        display: "block",
        justifyContent: "left",
        paddingLeft: "5px",
      }}
    >
      <span style={{ color: "#16A774" }}> help</span> --> Get help
      <br />
      <span style={{ color: "#16A774" }}> find {"<log_text>"}</span> --> Get
      results from analyser
      <br />
      <span style={{ color: "#16A774" }}>cls </span>--> clear screen
    </div>
  );

  async function make_axios_request() {}
  async function handleSubmit(event) {
    event.preventDefault();

    if (textc.trim() == "cls") {
      setData([]);
      setUpdater(!updater);
      setTextc("");
      return;
    }
    let result = null;
    let break_line = false;

    if (textc.trim() == "help") result = help;
    else if (textc.trim().length > 4 && textc.trim().substr(0, 4) == "find") {
      await axios
        .post("http://127.0.0.1:8000/", {
          msg: textc.substr(5),
          // headers: {
          //   "Content-Type": "application/json",
          // },
        })
        .then((u) => {
          console.log(u["data"]);
          result = "This might be related to '" + u["data"] + "' log file";
        })
        .catch((err) => {
          console.log(err);
        });
    } else {
      result = "Command Successfully excecuted";
      break_line = true;
    }

    const temp = data;
    temp.push({
      start: `${new Date().toLocaleString() + ""}\\hpe\\team4> `,
      command: textc.trim(),
      result: result,
      bl: break_line,
    });

    setData(temp);
    setUpdater(!updater);
    setTextc("");
    console.log(temp);
  }

  return (
    <div
      style={{
        backgroundColor: "black",
        color: "green",
        minHeight: "500px",
        overflow: "scroll",
        maxHeight: "500px",
      }}
    >
      <div
        style={{
          height: "30px",
          backgroundColor: "white",
          color: "black",
          display: "flex",
          justifyContent: "center",
          borderTopLeftRadius: "400px",
          borderTopRightRadius: "400px",
        }}
      >
        <div style={{ width: "100%" }}>
          <p
            style={{
              marginTop: "5px",
              fontWeight: 700,
              textAlign: "center",
              // position: "fixed",
              width: "100%",
            }}
          >
            {" "}
            Linux Kernel Log Analyser
          </p>
          {/* <br /> */}
          <div>
            <p style={{ color: "white", fontWeight: 100, fontSize: "12px" }}>
              Intelligent Kernel Log Analyser [hpe week 3]
              <br /> (NIE) - Team 4. All rights Reserved
            </p>

            <div
              style={{
                display: "block",
                justifyContent: "left",
                color: "white",
                fontSize: "12px",
                marginTop: "20px",
              }}
            >
              {updater ? (
                <div style={{ display: "block", justifyContent: "left" }}>
                  {data.map((item) => {
                    return (
                      <div
                        style={{ display: "block", justifyContent: "left" }}
                        key={item}
                      >
                        <div
                          style={{ display: "flex", justifyContent: "left" }}
                        >
                          {item["start"]}
                          {item["command"]}
                        </div>

                        {item["result"]}
                      </div>
                    );
                  })}
                </div>
              ) : (
                <div style={{ display: "block", justifyContent: "left" }}>
                  {data.map((item) => {
                    return (
                      <div
                        style={{ display: "block", justifyContent: "left" }}
                        key={item}
                      >
                        <div
                          style={{ display: "flex", justifyContent: "left" }}
                        >
                          {item["start"]}
                          {item["command"]}
                        </div>

                        {item["result"]}
                      </div>
                    );
                  })}
                </div>
              )}
              <div style={{ display: "flex", justifyContent: "left" }}>
                {new Date().toLocaleString() + ""}
                {"\\hpe\\team4>"}{" "}
                <form onSubmit={handleSubmit}>
                  <input
                    type="text"
                    name="command"
                    id="command"
                    value={textc}
                    onChange={async (e) => {
                      await setTextc(e.target.value);
                    }}
                    style={{
                      backgroundColor: "black",
                      color: "#16A774",
                      border: "0px solid black",
                      outline: "none",
                      "&focus": {
                        border: "0px solid black",
                      },
                      minWidth: "500px",
                    }}
                  ></input>
                </form>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
