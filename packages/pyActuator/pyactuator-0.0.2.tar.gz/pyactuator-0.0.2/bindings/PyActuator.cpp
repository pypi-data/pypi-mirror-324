#include <pybind11/pybind11.h>
#include "../orcaSDK/actuator.h"

namespace py = pybind11;

PYBIND11_MODULE(_pyActuator, m)
{
    m.doc() = "Python binding for the C++ orcaSDK";

     py::class_<orcaSDK::StreamData>(m, "StreamData")
        .def_readwrite("position", &orcaSDK::StreamData::position)
        .def_readwrite("force", &orcaSDK::StreamData::force)
        .def_readwrite("power", &orcaSDK::StreamData::power)
        .def_readwrite("temperature", &orcaSDK::StreamData::temperature)
        .def_readwrite("voltage", &orcaSDK::StreamData::voltage)
        .def_readwrite("errors", &orcaSDK::StreamData::errors);

     py::enum_<orcaSDK::MotorMode>(m, "MotorMode")
        .value("SleepMode", orcaSDK::SleepMode)
        .value("ForceMode", orcaSDK::ForceMode)
        .value("PositionMode", orcaSDK::PositionMode)
        .value("HapticMode", orcaSDK::HapticMode)
        .value("KinematicMode", orcaSDK::KinematicMode)
        .export_values();  // This allows access to the enum values in Python

     py::class_<orcaSDK::OrcaError>(m, "OrcaError")
          .def(py::init<int, std::string>(), py::arg("failure_type"), py::arg("error_message") = "")
          .def("__bool__", &orcaSDK::OrcaError::operator bool)
          .def("what", &orcaSDK::OrcaError::what)
          .def("__repr__", [](const orcaSDK::OrcaError& self) {
               return "<OrcaError failure=" + std::to_string(static_cast<bool>(self)) +
                    ", message='" + self.what() + "'>";
          });

            // Bind OrcaResult<int32_t>
     py::class_<orcaSDK::OrcaResult<int32_t>>(m, "OrcaResultInt32")
          //.def(py::init<>())  // Default constructor
          .def_readwrite("value", &orcaSDK::OrcaResult<int32_t>::value)
          .def_readwrite("error", &orcaSDK::OrcaResult<int32_t>::error);

     py::class_<orcaSDK::OrcaResult<int16_t>>(m, "OrcaResultInt16")
          //.def(py::init<>())  // Default constructor
          .def_readwrite("value", &orcaSDK::OrcaResult<int16_t>::value)
          .def_readwrite("error", &orcaSDK::OrcaResult<int16_t>::error);

     py::class_<orcaSDK::OrcaResult<uint16_t>>(m, "OrcaResultUInt16")
          //.def(py::init<>())  // Default constructor
          .def_readwrite("value", &orcaSDK::OrcaResult<uint16_t>::value)
          .def_readwrite("error", &orcaSDK::OrcaResult<uint16_t>::error);

     py::class_<orcaSDK::OrcaResult<std::vector<uint16_t>>>(m, "OrcaResultList")
          //.def(py::init<>())  // Default constructor
          .def_readwrite("value", &orcaSDK::OrcaResult<std::vector<uint16_t>>::value)
          .def_readwrite("error", &orcaSDK::OrcaResult<std::vector<uint16_t>>::error);

     py::class_<orcaSDK::OrcaResult<orcaSDK::MotorMode>>(m, "OrcaResultMotorMode")
          //.def(py::init<>())  // Default constructor
          .def_readwrite("value", &orcaSDK::OrcaResult<orcaSDK::MotorMode>::value)
          .def_readwrite("error", &orcaSDK::OrcaResult<orcaSDK::MotorMode>::error);




    py::enum_<orcaSDK::MessagePriority>(m, "MessagePriority")
        .value("important", orcaSDK::MessagePriority::important)
        .value("not_important", orcaSDK::MessagePriority::not_important)
        .export_values();
    
    py::class_<orcaSDK::Actuator>(m, "Actuator")
        .def(py::init<const char*, uint8_t>(), py::arg("name"), py::arg("modbus_server_address") = 1)

        .def(py::init<std::shared_ptr<orcaSDK::SerialInterface>, std::shared_ptr<orcaSDK::Clock>, const char*, uint8_t>(),

             py::arg("serial_interface"), py::arg("clock"), py::arg("name"), py::arg("modbus_server_address") = 1)

        .def("open_serial_port", &orcaSDK::Actuator::open_serial_port,
             py::arg("port_number"), py::arg("baud_rate") = orcaSDK::ModbusClient::kDefaultBaudRate,
             py::arg("interframe_delay") = orcaSDK::ModbusClient::kDefaultInterframeDelay_uS)

        .def("close_serial_port", &orcaSDK::Actuator::close_serial_port)

        .def("get_force_mN", &orcaSDK::Actuator::get_force_mN)

        .def("get_position_um", &orcaSDK::Actuator::get_position_um)

        .def("get_errors", &orcaSDK::Actuator::get_errors)

        .def("set_mode", &orcaSDK::Actuator::set_mode, py::arg("orca_mode"))

        .def("get_mode", &orcaSDK::Actuator::get_mode)

        .def("clear_errors", &orcaSDK::Actuator::clear_errors)

        .def("read_wide_register_blocking", &orcaSDK::Actuator::read_wide_register_blocking,
             py::arg("reg_address"), py::arg("priority") = orcaSDK::MessagePriority::important)

        .def("read_register_blocking", &orcaSDK::Actuator::read_register_blocking,
             py::arg("reg_address"), py::arg("priority") = orcaSDK::MessagePriority::important)

        .def("read_multiple_registers_blocking", &orcaSDK::Actuator::read_multiple_registers_blocking,
             py::arg("reg_start_address"), py::arg("num_registers"), py::arg("priority") = orcaSDK::MessagePriority::important)

        .def("write_register_blocking", &orcaSDK::Actuator::write_register_blocking,
             py::arg("reg_address"), py::arg("write_data"), py::arg("priority") = orcaSDK::MessagePriority::important)

        .def("write_wide_register_blocking", &orcaSDK::Actuator::write_wide_register_blocking,
             py::arg("reg_address"), py::arg("write_data"), py::arg("priority") = orcaSDK::MessagePriority::important)

        .def("write_multiple_registers_blocking", &orcaSDK::Actuator::write_multiple_registers_blocking,
             py::arg("reg_start_address"), py::arg("num_registers"), py::arg("write_data"), py::arg("priority") = orcaSDK::MessagePriority::important)

        .def("read_write_multiple_registers_blocking", &orcaSDK::Actuator::read_write_multiple_registers_blocking,
             py::arg("read_starting_address"), py::arg("read_num_registers"),
             py::arg("write_starting_address"), py::arg("write_num_registers"),
             py::arg("write_data"), py::arg("priority") = orcaSDK::MessagePriority::important)

        .def("begin_serial_logging", py::overload_cast<const std::string&>(&orcaSDK::Actuator::begin_serial_logging),
             py::arg("log_name"))

        .def("begin_serial_logging", py::overload_cast<const std::string&, std::shared_ptr<orcaSDK::LogInterface>>(&orcaSDK::Actuator::begin_serial_logging),
             py::arg("log_name"), py::arg("log"))

        .def("run", &orcaSDK::Actuator::run)

        .def("enable_stream", &orcaSDK::Actuator::enable_stream)

        .def("disable_stream", &orcaSDK::Actuator::disable_stream)

        .def("set_streamed_force_mN", &orcaSDK::Actuator::set_streamed_force_mN, py::arg("force"))

        .def("set_streamed_position_um", &orcaSDK::Actuator::set_streamed_position_um, py::arg("position"))

        .def("update_haptic_stream_effects", &orcaSDK::Actuator::update_haptic_stream_effects, py::arg("effects"))

        .def("get_power_W", &orcaSDK::Actuator::get_power_W)

        .def("get_temperature_C", &orcaSDK::Actuator::get_temperature_C)

        .def("get_voltage_mV", &orcaSDK::Actuator::get_voltage_mV)

        .def("get_stream_data", [](orcaSDK::Actuator& actuator) { return actuator.stream_cache; })

        .def_readonly("name", &orcaSDK::Actuator::name);

}