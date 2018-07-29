
## streamiot-mvp d --  register and watch all your IOT devices on the blockchain


**Stack:**
- Docker v1.11.1 +
- Python API -> Flask / Flask-RESTful  (Python 3.7 )

**Getting up and running:**
- Install Docker Toolbox - https://docs.docker.com/engine/getstarted/step_one/

- Clone the streamiot_mvp_1 repository

```bash
$ git clone https://github.com/streamchain-iot/fed_stream_node.git

$ cd fed_stream_node

```
- Run the following from a terminal within this project root:

    ` sh build.sh`
   
- Verify if connecting
   
   ` curl http://localhost:5000/get-devices/####SOMEKEY#### '
