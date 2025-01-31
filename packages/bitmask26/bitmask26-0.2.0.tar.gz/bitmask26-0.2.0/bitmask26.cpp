#include <cstdint>
#include <vector>
#include <sstream>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

class Bitmask26 {
private:
  uint32_t mask;

public:
  Bitmask26(const std::string &s) : mask(0) {
    for (auto c : s) {
      if (c >= 'a' && c <= 'z') {
        mask |= (1 << (c - 'a'));
      } else if (c >= 'A' && c <= 'Z') {
        mask |= (1 << (c - 'A'));
      }
    }
  }

  Bitmask26(const uint32_t mask) {
    this->mask = mask;
  }

  auto operator==(const Bitmask26 &other) const {
    return mask == other.mask;
  }

  auto hash() const {
    return std::hash<uint32_t>{}(mask);
  }

  auto repr() const {
    std::ostringstream out;
    out << "bm26[";
    for (int i = 0; i < 26; ++i) {
      if ((1 << i) & mask) {
        out << static_cast<char>('a' + i);
      }
    }
    out << ']';
    return out.str();
  }

  auto operator>=(const Bitmask26 &other) const {
    return (mask | other.mask) == mask;
  }

  auto static __getstate__(const Bitmask26 &b) {
    return py::make_tuple(b.mask);
  }

  auto static __setstate__(py::tuple state) {
    if (state.size() != 1) {
      throw std::runtime_error("Invalid state!");
    }
    auto mask = state[0].cast<uint32_t>();
    return Bitmask26(mask);
  }

  py::buffer_info get_buffer() const {
    return py::buffer_info(
      (void*)&mask,
      sizeof(uint32_t),
      py::format_descriptor<uint32_t>::format(),
      1,
      {1},
      {sizeof(uint32_t)}
    );
  }

};

PYBIND11_MODULE(bitmask26, m) {
  py::class_<Bitmask26>(m, "Bitmask26")
    .def(py::init<const std::string &>(), "Constructs a Bitmask26 from a word.")
    .def("__eq__", &Bitmask26::operator==)
    .def("__hash__", &Bitmask26::hash)
    .def("__repr__", &Bitmask26::repr)
    .def("__ge__", &Bitmask26::operator>=)
    .def(py::pickle(&Bitmask26::__getstate__, &Bitmask26::__setstate__));
}
