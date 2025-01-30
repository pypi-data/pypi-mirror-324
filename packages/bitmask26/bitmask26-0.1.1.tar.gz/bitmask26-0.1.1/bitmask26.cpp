#include <cstdint>
#include <vector>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

namespace py = pybind11;

class Bitmask26 {
private:
  uint32_t mask;
  mutable uint32_t nmask;
  mutable bool nmask_computed;

public:
  Bitmask26(const std::string &s) : mask(0), nmask(0), nmask_computed(false) {
    for (auto c : s) {
      if (c >= 'a' && c <= 'z') {
        mask |= (1 << (c - 'a'));
      } else if (c >= 'A' && c <= 'Z') {
        mask |= (1 << (c - 'A'));
      } 
    }
  }

  bool operator==(const Bitmask26 &other) const {
    return mask == other.mask;
  }

  std::size_t hash() const {
    return std::hash<uint32_t>{}(mask);
  }

  bool operator>=(const Bitmask26 &other) const {
    if (!nmask_computed) {
      nmask = ~mask;
      nmask_computed = true;
    }
    return !(nmask & other.mask);
  }
};

PYBIND11_MODULE(bitmask26, m) {
  py::class_<Bitmask26>(m, "Bitmask26")
    .def(py::init<const std::string &>(), "Constructs a Bitmask26 from a word.")
    .def("__eq__", &Bitmask26::operator==)
    .def("__hash__", &Bitmask26::hash)
    .def("__ge__", &Bitmask26::operator>=);
}
