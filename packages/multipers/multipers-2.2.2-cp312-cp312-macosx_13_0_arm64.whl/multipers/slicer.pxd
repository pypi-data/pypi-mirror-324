
cimport numpy as cnp

# SequentialDataset and its two concrete subclasses are (optionally randomized)
# iterators over the rows of a matrix X and corresponding target values y.

from libcpp.utility cimport pair 
from libcpp cimport bool, int, float
from libcpp.vector cimport vector


from libc.stdint cimport intptr_t, uint16_t, uint32_t, int32_t, uint64_t, int64_t
from cython cimport uint

import numpy as np
python_value_type=np.float32
from libcpp.string cimport string

cdef extern from "Simplex_tree_multi_interface.h" namespace "Gudhi::multiparameter::python_interface":
    cdef cppclass Simplex_tree_multi_interface[F=*, value_type=*]:
        pass

from multipers.filtrations cimport *
ctypedef  vector[uint] cycle_type ## its the cycle type of matrix


#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_Matrix0_vine_i32 "TrucPythonInterface<BackendsEnum::Matrix,true,true,int32_t,Available_columns::INTRUSIVE_SET>":
      ctypedef int32_t value_type

      C_KSlicer_Matrix0_vine_i32()

      C_KSlicer_Matrix0_vine_i32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[int32_t]]&)

      C_KSlicer_Matrix0_vine_i32& operator=(const C_KSlicer_Matrix0_vine_i32&)
      vector[vector[pair[int32_t, int32_t]]] get_barcode() nogil
      void push_to(const Line[int32_t]&) nogil
      void set_one_filtration(const vector[int32_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int32_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int32_t], One_critical_filtration[int32_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int32_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int32_t]], bool) nogil
      vector[Multi_critical_filtration[int32_t]]& get_filtrations() nogil
      C_KSlicer_Matrix0_vine_i32 coarsen_on_grid(vector[vector[int32_t]]) nogil
      void vineyard_update() nogil
      vector[vector[vector[vector[unsigned int]]]] get_representative_cycles(bool, bool) nogil
      vector[uint32_t] get_current_order() nogil
      void add_generator(const One_critical_filtration[int32_t] &) nogil


      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[vector[int32_t]]) nogil
      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[pair[vector[int32_t],vector[int32_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_Matrix1_vine_i32 "TrucPythonInterface<BackendsEnum::Matrix,true,true,int32_t,Available_columns::SMALL_VECTOR>":
      ctypedef int32_t value_type

      C_KSlicer_Matrix1_vine_i32()

      C_KSlicer_Matrix1_vine_i32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[int32_t]]&)

      C_KSlicer_Matrix1_vine_i32& operator=(const C_KSlicer_Matrix1_vine_i32&)
      vector[vector[pair[int32_t, int32_t]]] get_barcode() nogil
      void push_to(const Line[int32_t]&) nogil
      void set_one_filtration(const vector[int32_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int32_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int32_t], One_critical_filtration[int32_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int32_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int32_t]], bool) nogil
      vector[Multi_critical_filtration[int32_t]]& get_filtrations() nogil
      C_KSlicer_Matrix1_vine_i32 coarsen_on_grid(vector[vector[int32_t]]) nogil
      void vineyard_update() nogil
      vector[vector[vector[vector[unsigned int]]]] get_representative_cycles(bool, bool) nogil
      vector[uint32_t] get_current_order() nogil
      void add_generator(const One_critical_filtration[int32_t] &) nogil


      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[vector[int32_t]]) nogil
      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[pair[vector[int32_t],vector[int32_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_Matrix0_vine_i64 "TrucPythonInterface<BackendsEnum::Matrix,true,true,int64_t,Available_columns::INTRUSIVE_SET>":
      ctypedef int64_t value_type

      C_KSlicer_Matrix0_vine_i64()

      C_KSlicer_Matrix0_vine_i64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[int64_t]]&)

      C_KSlicer_Matrix0_vine_i64& operator=(const C_KSlicer_Matrix0_vine_i64&)
      vector[vector[pair[int64_t, int64_t]]] get_barcode() nogil
      void push_to(const Line[int64_t]&) nogil
      void set_one_filtration(const vector[int64_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int64_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int64_t], One_critical_filtration[int64_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int64_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int64_t]], bool) nogil
      vector[Multi_critical_filtration[int64_t]]& get_filtrations() nogil
      C_KSlicer_Matrix0_vine_i32 coarsen_on_grid(vector[vector[int64_t]]) nogil
      void vineyard_update() nogil
      vector[vector[vector[vector[unsigned int]]]] get_representative_cycles(bool, bool) nogil
      vector[uint32_t] get_current_order() nogil
      void add_generator(const One_critical_filtration[int64_t] &) nogil


      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[vector[int64_t]]) nogil
      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[pair[vector[int64_t],vector[int64_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_Matrix1_vine_i64 "TrucPythonInterface<BackendsEnum::Matrix,true,true,int64_t,Available_columns::SMALL_VECTOR>":
      ctypedef int64_t value_type

      C_KSlicer_Matrix1_vine_i64()

      C_KSlicer_Matrix1_vine_i64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[int64_t]]&)

      C_KSlicer_Matrix1_vine_i64& operator=(const C_KSlicer_Matrix1_vine_i64&)
      vector[vector[pair[int64_t, int64_t]]] get_barcode() nogil
      void push_to(const Line[int64_t]&) nogil
      void set_one_filtration(const vector[int64_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int64_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int64_t], One_critical_filtration[int64_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int64_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int64_t]], bool) nogil
      vector[Multi_critical_filtration[int64_t]]& get_filtrations() nogil
      C_KSlicer_Matrix1_vine_i32 coarsen_on_grid(vector[vector[int64_t]]) nogil
      void vineyard_update() nogil
      vector[vector[vector[vector[unsigned int]]]] get_representative_cycles(bool, bool) nogil
      vector[uint32_t] get_current_order() nogil
      void add_generator(const One_critical_filtration[int64_t] &) nogil


      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[vector[int64_t]]) nogil
      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[pair[vector[int64_t],vector[int64_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_Matrix0_vine_f32 "TrucPythonInterface<BackendsEnum::Matrix,true,true,float,Available_columns::INTRUSIVE_SET>":
      ctypedef float value_type

      C_KSlicer_Matrix0_vine_f32()

      C_KSlicer_Matrix0_vine_f32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[float]]&)

      C_KSlicer_Matrix0_vine_f32& operator=(const C_KSlicer_Matrix0_vine_f32&)
      vector[vector[pair[float, float]]] get_barcode() nogil
      void push_to(const Line[float]&) nogil
      void set_one_filtration(const vector[float]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[float] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[float], One_critical_filtration[float]] get_bounding_box() except + nogil
      vector[One_critical_filtration[float]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[float]], bool) nogil
      vector[Multi_critical_filtration[float]]& get_filtrations() nogil
      C_KSlicer_Matrix0_vine_i32 coarsen_on_grid(vector[vector[float]]) nogil
      void vineyard_update() nogil
      vector[vector[vector[vector[unsigned int]]]] get_representative_cycles(bool, bool) nogil
      vector[uint32_t] get_current_order() nogil
      void add_generator(const One_critical_filtration[float] &) nogil


      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[vector[float]]) nogil
      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[pair[vector[float],vector[float]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_Matrix1_vine_f32 "TrucPythonInterface<BackendsEnum::Matrix,true,true,float,Available_columns::SMALL_VECTOR>":
      ctypedef float value_type

      C_KSlicer_Matrix1_vine_f32()

      C_KSlicer_Matrix1_vine_f32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[float]]&)

      C_KSlicer_Matrix1_vine_f32& operator=(const C_KSlicer_Matrix1_vine_f32&)
      vector[vector[pair[float, float]]] get_barcode() nogil
      void push_to(const Line[float]&) nogil
      void set_one_filtration(const vector[float]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[float] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[float], One_critical_filtration[float]] get_bounding_box() except + nogil
      vector[One_critical_filtration[float]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[float]], bool) nogil
      vector[Multi_critical_filtration[float]]& get_filtrations() nogil
      C_KSlicer_Matrix1_vine_i32 coarsen_on_grid(vector[vector[float]]) nogil
      void vineyard_update() nogil
      vector[vector[vector[vector[unsigned int]]]] get_representative_cycles(bool, bool) nogil
      vector[uint32_t] get_current_order() nogil
      void add_generator(const One_critical_filtration[float] &) nogil


      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[vector[float]]) nogil
      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[pair[vector[float],vector[float]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_Matrix0_vine_f64 "TrucPythonInterface<BackendsEnum::Matrix,true,true,double,Available_columns::INTRUSIVE_SET>":
      ctypedef double value_type

      C_KSlicer_Matrix0_vine_f64()

      C_KSlicer_Matrix0_vine_f64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[double]]&)

      C_KSlicer_Matrix0_vine_f64& operator=(const C_KSlicer_Matrix0_vine_f64&)
      vector[vector[pair[double, double]]] get_barcode() nogil
      void push_to(const Line[double]&) nogil
      void set_one_filtration(const vector[double]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[double] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[double], One_critical_filtration[double]] get_bounding_box() except + nogil
      vector[One_critical_filtration[double]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[double]], bool) nogil
      vector[Multi_critical_filtration[double]]& get_filtrations() nogil
      C_KSlicer_Matrix0_vine_i32 coarsen_on_grid(vector[vector[double]]) nogil
      void vineyard_update() nogil
      vector[vector[vector[vector[unsigned int]]]] get_representative_cycles(bool, bool) nogil
      vector[uint32_t] get_current_order() nogil
      void add_generator(const One_critical_filtration[double] &) nogil


      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[vector[double]]) nogil
      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[pair[vector[double],vector[double]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_Matrix1_vine_f64 "TrucPythonInterface<BackendsEnum::Matrix,true,true,double,Available_columns::SMALL_VECTOR>":
      ctypedef double value_type

      C_KSlicer_Matrix1_vine_f64()

      C_KSlicer_Matrix1_vine_f64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[double]]&)

      C_KSlicer_Matrix1_vine_f64& operator=(const C_KSlicer_Matrix1_vine_f64&)
      vector[vector[pair[double, double]]] get_barcode() nogil
      void push_to(const Line[double]&) nogil
      void set_one_filtration(const vector[double]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[double] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[double], One_critical_filtration[double]] get_bounding_box() except + nogil
      vector[One_critical_filtration[double]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[double]], bool) nogil
      vector[Multi_critical_filtration[double]]& get_filtrations() nogil
      C_KSlicer_Matrix1_vine_i32 coarsen_on_grid(vector[vector[double]]) nogil
      void vineyard_update() nogil
      vector[vector[vector[vector[unsigned int]]]] get_representative_cycles(bool, bool) nogil
      vector[uint32_t] get_current_order() nogil
      void add_generator(const One_critical_filtration[double] &) nogil


      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[vector[double]]) nogil
      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[pair[vector[double],vector[double]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_Matrix0_vine_i32 "TrucPythonInterface<BackendsEnum::Matrix,true,false,int32_t,Available_columns::INTRUSIVE_SET>":
      ctypedef int32_t value_type

      C_Slicer_Matrix0_vine_i32()

      C_Slicer_Matrix0_vine_i32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[int32_t]]&)

      C_Slicer_Matrix0_vine_i32& operator=(const C_Slicer_Matrix0_vine_i32&)
      vector[vector[pair[int32_t, int32_t]]] get_barcode() nogil
      void push_to(const Line[int32_t]&) nogil
      void set_one_filtration(const vector[int32_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int32_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int32_t], One_critical_filtration[int32_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int32_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int32_t]], bool) nogil
      vector[One_critical_filtration[int32_t]]& get_filtrations() nogil
      C_Slicer_Matrix0_vine_i32 coarsen_on_grid(vector[vector[int32_t]]) nogil
      void vineyard_update() nogil
      vector[vector[vector[vector[unsigned int]]]] get_representative_cycles(bool, bool) nogil
      vector[uint32_t] get_current_order() nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[vector[int32_t]]) nogil
      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[pair[vector[int32_t],vector[int32_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_Matrix1_vine_i32 "TrucPythonInterface<BackendsEnum::Matrix,true,false,int32_t,Available_columns::SMALL_VECTOR>":
      ctypedef int32_t value_type

      C_Slicer_Matrix1_vine_i32()

      C_Slicer_Matrix1_vine_i32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[int32_t]]&)

      C_Slicer_Matrix1_vine_i32& operator=(const C_Slicer_Matrix1_vine_i32&)
      vector[vector[pair[int32_t, int32_t]]] get_barcode() nogil
      void push_to(const Line[int32_t]&) nogil
      void set_one_filtration(const vector[int32_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int32_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int32_t], One_critical_filtration[int32_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int32_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int32_t]], bool) nogil
      vector[One_critical_filtration[int32_t]]& get_filtrations() nogil
      C_Slicer_Matrix1_vine_i32 coarsen_on_grid(vector[vector[int32_t]]) nogil
      void vineyard_update() nogil
      vector[vector[vector[vector[unsigned int]]]] get_representative_cycles(bool, bool) nogil
      vector[uint32_t] get_current_order() nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[vector[int32_t]]) nogil
      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[pair[vector[int32_t],vector[int32_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_Matrix0_vine_i64 "TrucPythonInterface<BackendsEnum::Matrix,true,false,int64_t,Available_columns::INTRUSIVE_SET>":
      ctypedef int64_t value_type

      C_Slicer_Matrix0_vine_i64()

      C_Slicer_Matrix0_vine_i64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[int64_t]]&)

      C_Slicer_Matrix0_vine_i64& operator=(const C_Slicer_Matrix0_vine_i64&)
      vector[vector[pair[int64_t, int64_t]]] get_barcode() nogil
      void push_to(const Line[int64_t]&) nogil
      void set_one_filtration(const vector[int64_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int64_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int64_t], One_critical_filtration[int64_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int64_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int64_t]], bool) nogil
      vector[One_critical_filtration[int64_t]]& get_filtrations() nogil
      C_Slicer_Matrix0_vine_i32 coarsen_on_grid(vector[vector[int64_t]]) nogil
      void vineyard_update() nogil
      vector[vector[vector[vector[unsigned int]]]] get_representative_cycles(bool, bool) nogil
      vector[uint32_t] get_current_order() nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[vector[int64_t]]) nogil
      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[pair[vector[int64_t],vector[int64_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_Matrix1_vine_i64 "TrucPythonInterface<BackendsEnum::Matrix,true,false,int64_t,Available_columns::SMALL_VECTOR>":
      ctypedef int64_t value_type

      C_Slicer_Matrix1_vine_i64()

      C_Slicer_Matrix1_vine_i64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[int64_t]]&)

      C_Slicer_Matrix1_vine_i64& operator=(const C_Slicer_Matrix1_vine_i64&)
      vector[vector[pair[int64_t, int64_t]]] get_barcode() nogil
      void push_to(const Line[int64_t]&) nogil
      void set_one_filtration(const vector[int64_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int64_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int64_t], One_critical_filtration[int64_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int64_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int64_t]], bool) nogil
      vector[One_critical_filtration[int64_t]]& get_filtrations() nogil
      C_Slicer_Matrix1_vine_i32 coarsen_on_grid(vector[vector[int64_t]]) nogil
      void vineyard_update() nogil
      vector[vector[vector[vector[unsigned int]]]] get_representative_cycles(bool, bool) nogil
      vector[uint32_t] get_current_order() nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[vector[int64_t]]) nogil
      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[pair[vector[int64_t],vector[int64_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_Matrix0_vine_f32 "TrucPythonInterface<BackendsEnum::Matrix,true,false,float,Available_columns::INTRUSIVE_SET>":
      ctypedef float value_type

      C_Slicer_Matrix0_vine_f32()

      C_Slicer_Matrix0_vine_f32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[float]]&)

      C_Slicer_Matrix0_vine_f32& operator=(const C_Slicer_Matrix0_vine_f32&)
      vector[vector[pair[float, float]]] get_barcode() nogil
      void push_to(const Line[float]&) nogil
      void set_one_filtration(const vector[float]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[float] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[float], One_critical_filtration[float]] get_bounding_box() except + nogil
      vector[One_critical_filtration[float]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[float]], bool) nogil
      vector[One_critical_filtration[float]]& get_filtrations() nogil
      C_Slicer_Matrix0_vine_i32 coarsen_on_grid(vector[vector[float]]) nogil
      void vineyard_update() nogil
      vector[vector[vector[vector[unsigned int]]]] get_representative_cycles(bool, bool) nogil
      vector[uint32_t] get_current_order() nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[vector[float]]) nogil
      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[pair[vector[float],vector[float]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_Matrix1_vine_f32 "TrucPythonInterface<BackendsEnum::Matrix,true,false,float,Available_columns::SMALL_VECTOR>":
      ctypedef float value_type

      C_Slicer_Matrix1_vine_f32()

      C_Slicer_Matrix1_vine_f32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[float]]&)

      C_Slicer_Matrix1_vine_f32& operator=(const C_Slicer_Matrix1_vine_f32&)
      vector[vector[pair[float, float]]] get_barcode() nogil
      void push_to(const Line[float]&) nogil
      void set_one_filtration(const vector[float]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[float] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[float], One_critical_filtration[float]] get_bounding_box() except + nogil
      vector[One_critical_filtration[float]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[float]], bool) nogil
      vector[One_critical_filtration[float]]& get_filtrations() nogil
      C_Slicer_Matrix1_vine_i32 coarsen_on_grid(vector[vector[float]]) nogil
      void vineyard_update() nogil
      vector[vector[vector[vector[unsigned int]]]] get_representative_cycles(bool, bool) nogil
      vector[uint32_t] get_current_order() nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[vector[float]]) nogil
      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[pair[vector[float],vector[float]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_Matrix0_vine_f64 "TrucPythonInterface<BackendsEnum::Matrix,true,false,double,Available_columns::INTRUSIVE_SET>":
      ctypedef double value_type

      C_Slicer_Matrix0_vine_f64()

      C_Slicer_Matrix0_vine_f64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[double]]&)

      C_Slicer_Matrix0_vine_f64& operator=(const C_Slicer_Matrix0_vine_f64&)
      vector[vector[pair[double, double]]] get_barcode() nogil
      void push_to(const Line[double]&) nogil
      void set_one_filtration(const vector[double]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[double] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[double], One_critical_filtration[double]] get_bounding_box() except + nogil
      vector[One_critical_filtration[double]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[double]], bool) nogil
      vector[One_critical_filtration[double]]& get_filtrations() nogil
      C_Slicer_Matrix0_vine_i32 coarsen_on_grid(vector[vector[double]]) nogil
      void vineyard_update() nogil
      vector[vector[vector[vector[unsigned int]]]] get_representative_cycles(bool, bool) nogil
      vector[uint32_t] get_current_order() nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[vector[double]]) nogil
      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[pair[vector[double],vector[double]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_Matrix1_vine_f64 "TrucPythonInterface<BackendsEnum::Matrix,true,false,double,Available_columns::SMALL_VECTOR>":
      ctypedef double value_type

      C_Slicer_Matrix1_vine_f64()

      C_Slicer_Matrix1_vine_f64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[double]]&)

      C_Slicer_Matrix1_vine_f64& operator=(const C_Slicer_Matrix1_vine_f64&)
      vector[vector[pair[double, double]]] get_barcode() nogil
      void push_to(const Line[double]&) nogil
      void set_one_filtration(const vector[double]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[double] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[double], One_critical_filtration[double]] get_bounding_box() except + nogil
      vector[One_critical_filtration[double]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[double]], bool) nogil
      vector[One_critical_filtration[double]]& get_filtrations() nogil
      C_Slicer_Matrix1_vine_i32 coarsen_on_grid(vector[vector[double]]) nogil
      void vineyard_update() nogil
      vector[vector[vector[vector[unsigned int]]]] get_representative_cycles(bool, bool) nogil
      vector[uint32_t] get_current_order() nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[vector[double]]) nogil
      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[pair[vector[double],vector[double]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_Matrix0_i32 "TrucPythonInterface<BackendsEnum::Matrix,false,true,int32_t,Available_columns::INTRUSIVE_SET>":
      ctypedef int32_t value_type

      C_KSlicer_Matrix0_i32()

      C_KSlicer_Matrix0_i32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[int32_t]]&)

      C_KSlicer_Matrix0_i32& operator=(const C_KSlicer_Matrix0_i32&)
      vector[vector[pair[int32_t, int32_t]]] get_barcode() nogil
      void push_to(const Line[int32_t]&) nogil
      void set_one_filtration(const vector[int32_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int32_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int32_t], One_critical_filtration[int32_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int32_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int32_t]], bool) nogil
      vector[Multi_critical_filtration[int32_t]]& get_filtrations() nogil
      C_KSlicer_Matrix0_i32 coarsen_on_grid(vector[vector[int32_t]]) nogil
      void add_generator(const One_critical_filtration[int32_t] &) nogil


      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[vector[int32_t]]) nogil
      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[pair[vector[int32_t],vector[int32_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_Matrix1_i32 "TrucPythonInterface<BackendsEnum::Matrix,false,true,int32_t,Available_columns::SMALL_VECTOR>":
      ctypedef int32_t value_type

      C_KSlicer_Matrix1_i32()

      C_KSlicer_Matrix1_i32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[int32_t]]&)

      C_KSlicer_Matrix1_i32& operator=(const C_KSlicer_Matrix1_i32&)
      vector[vector[pair[int32_t, int32_t]]] get_barcode() nogil
      void push_to(const Line[int32_t]&) nogil
      void set_one_filtration(const vector[int32_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int32_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int32_t], One_critical_filtration[int32_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int32_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int32_t]], bool) nogil
      vector[Multi_critical_filtration[int32_t]]& get_filtrations() nogil
      C_KSlicer_Matrix1_i32 coarsen_on_grid(vector[vector[int32_t]]) nogil
      void add_generator(const One_critical_filtration[int32_t] &) nogil


      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[vector[int32_t]]) nogil
      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[pair[vector[int32_t],vector[int32_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_Matrix0_i64 "TrucPythonInterface<BackendsEnum::Matrix,false,true,int64_t,Available_columns::INTRUSIVE_SET>":
      ctypedef int64_t value_type

      C_KSlicer_Matrix0_i64()

      C_KSlicer_Matrix0_i64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[int64_t]]&)

      C_KSlicer_Matrix0_i64& operator=(const C_KSlicer_Matrix0_i64&)
      vector[vector[pair[int64_t, int64_t]]] get_barcode() nogil
      void push_to(const Line[int64_t]&) nogil
      void set_one_filtration(const vector[int64_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int64_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int64_t], One_critical_filtration[int64_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int64_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int64_t]], bool) nogil
      vector[Multi_critical_filtration[int64_t]]& get_filtrations() nogil
      C_KSlicer_Matrix0_i32 coarsen_on_grid(vector[vector[int64_t]]) nogil
      void add_generator(const One_critical_filtration[int64_t] &) nogil


      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[vector[int64_t]]) nogil
      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[pair[vector[int64_t],vector[int64_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_Matrix1_i64 "TrucPythonInterface<BackendsEnum::Matrix,false,true,int64_t,Available_columns::SMALL_VECTOR>":
      ctypedef int64_t value_type

      C_KSlicer_Matrix1_i64()

      C_KSlicer_Matrix1_i64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[int64_t]]&)

      C_KSlicer_Matrix1_i64& operator=(const C_KSlicer_Matrix1_i64&)
      vector[vector[pair[int64_t, int64_t]]] get_barcode() nogil
      void push_to(const Line[int64_t]&) nogil
      void set_one_filtration(const vector[int64_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int64_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int64_t], One_critical_filtration[int64_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int64_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int64_t]], bool) nogil
      vector[Multi_critical_filtration[int64_t]]& get_filtrations() nogil
      C_KSlicer_Matrix1_i32 coarsen_on_grid(vector[vector[int64_t]]) nogil
      void add_generator(const One_critical_filtration[int64_t] &) nogil


      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[vector[int64_t]]) nogil
      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[pair[vector[int64_t],vector[int64_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_Matrix0_f32 "TrucPythonInterface<BackendsEnum::Matrix,false,true,float,Available_columns::INTRUSIVE_SET>":
      ctypedef float value_type

      C_KSlicer_Matrix0_f32()

      C_KSlicer_Matrix0_f32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[float]]&)

      C_KSlicer_Matrix0_f32& operator=(const C_KSlicer_Matrix0_f32&)
      vector[vector[pair[float, float]]] get_barcode() nogil
      void push_to(const Line[float]&) nogil
      void set_one_filtration(const vector[float]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[float] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[float], One_critical_filtration[float]] get_bounding_box() except + nogil
      vector[One_critical_filtration[float]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[float]], bool) nogil
      vector[Multi_critical_filtration[float]]& get_filtrations() nogil
      C_KSlicer_Matrix0_i32 coarsen_on_grid(vector[vector[float]]) nogil
      void add_generator(const One_critical_filtration[float] &) nogil


      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[vector[float]]) nogil
      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[pair[vector[float],vector[float]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_Matrix1_f32 "TrucPythonInterface<BackendsEnum::Matrix,false,true,float,Available_columns::SMALL_VECTOR>":
      ctypedef float value_type

      C_KSlicer_Matrix1_f32()

      C_KSlicer_Matrix1_f32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[float]]&)

      C_KSlicer_Matrix1_f32& operator=(const C_KSlicer_Matrix1_f32&)
      vector[vector[pair[float, float]]] get_barcode() nogil
      void push_to(const Line[float]&) nogil
      void set_one_filtration(const vector[float]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[float] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[float], One_critical_filtration[float]] get_bounding_box() except + nogil
      vector[One_critical_filtration[float]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[float]], bool) nogil
      vector[Multi_critical_filtration[float]]& get_filtrations() nogil
      C_KSlicer_Matrix1_i32 coarsen_on_grid(vector[vector[float]]) nogil
      void add_generator(const One_critical_filtration[float] &) nogil


      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[vector[float]]) nogil
      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[pair[vector[float],vector[float]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_Matrix0_f64 "TrucPythonInterface<BackendsEnum::Matrix,false,true,double,Available_columns::INTRUSIVE_SET>":
      ctypedef double value_type

      C_KSlicer_Matrix0_f64()

      C_KSlicer_Matrix0_f64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[double]]&)

      C_KSlicer_Matrix0_f64& operator=(const C_KSlicer_Matrix0_f64&)
      vector[vector[pair[double, double]]] get_barcode() nogil
      void push_to(const Line[double]&) nogil
      void set_one_filtration(const vector[double]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[double] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[double], One_critical_filtration[double]] get_bounding_box() except + nogil
      vector[One_critical_filtration[double]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[double]], bool) nogil
      vector[Multi_critical_filtration[double]]& get_filtrations() nogil
      C_KSlicer_Matrix0_i32 coarsen_on_grid(vector[vector[double]]) nogil
      void add_generator(const One_critical_filtration[double] &) nogil


      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[vector[double]]) nogil
      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[pair[vector[double],vector[double]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_Matrix1_f64 "TrucPythonInterface<BackendsEnum::Matrix,false,true,double,Available_columns::SMALL_VECTOR>":
      ctypedef double value_type

      C_KSlicer_Matrix1_f64()

      C_KSlicer_Matrix1_f64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[double]]&)

      C_KSlicer_Matrix1_f64& operator=(const C_KSlicer_Matrix1_f64&)
      vector[vector[pair[double, double]]] get_barcode() nogil
      void push_to(const Line[double]&) nogil
      void set_one_filtration(const vector[double]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[double] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[double], One_critical_filtration[double]] get_bounding_box() except + nogil
      vector[One_critical_filtration[double]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[double]], bool) nogil
      vector[Multi_critical_filtration[double]]& get_filtrations() nogil
      C_KSlicer_Matrix1_i32 coarsen_on_grid(vector[vector[double]]) nogil
      void add_generator(const One_critical_filtration[double] &) nogil


      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[vector[double]]) nogil
      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[pair[vector[double],vector[double]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_Matrix0_i32 "TrucPythonInterface<BackendsEnum::Matrix,false,false,int32_t,Available_columns::INTRUSIVE_SET>":
      ctypedef int32_t value_type

      C_Slicer_Matrix0_i32()

      C_Slicer_Matrix0_i32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[int32_t]]&)

      C_Slicer_Matrix0_i32& operator=(const C_Slicer_Matrix0_i32&)
      vector[vector[pair[int32_t, int32_t]]] get_barcode() nogil
      void push_to(const Line[int32_t]&) nogil
      void set_one_filtration(const vector[int32_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int32_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int32_t], One_critical_filtration[int32_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int32_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int32_t]], bool) nogil
      vector[One_critical_filtration[int32_t]]& get_filtrations() nogil
      C_Slicer_Matrix0_i32 coarsen_on_grid(vector[vector[int32_t]]) nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[vector[int32_t]]) nogil
      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[pair[vector[int32_t],vector[int32_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_Matrix1_i32 "TrucPythonInterface<BackendsEnum::Matrix,false,false,int32_t,Available_columns::SMALL_VECTOR>":
      ctypedef int32_t value_type

      C_Slicer_Matrix1_i32()

      C_Slicer_Matrix1_i32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[int32_t]]&)

      C_Slicer_Matrix1_i32& operator=(const C_Slicer_Matrix1_i32&)
      vector[vector[pair[int32_t, int32_t]]] get_barcode() nogil
      void push_to(const Line[int32_t]&) nogil
      void set_one_filtration(const vector[int32_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int32_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int32_t], One_critical_filtration[int32_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int32_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int32_t]], bool) nogil
      vector[One_critical_filtration[int32_t]]& get_filtrations() nogil
      C_Slicer_Matrix1_i32 coarsen_on_grid(vector[vector[int32_t]]) nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[vector[int32_t]]) nogil
      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[pair[vector[int32_t],vector[int32_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_Matrix0_i64 "TrucPythonInterface<BackendsEnum::Matrix,false,false,int64_t,Available_columns::INTRUSIVE_SET>":
      ctypedef int64_t value_type

      C_Slicer_Matrix0_i64()

      C_Slicer_Matrix0_i64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[int64_t]]&)

      C_Slicer_Matrix0_i64& operator=(const C_Slicer_Matrix0_i64&)
      vector[vector[pair[int64_t, int64_t]]] get_barcode() nogil
      void push_to(const Line[int64_t]&) nogil
      void set_one_filtration(const vector[int64_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int64_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int64_t], One_critical_filtration[int64_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int64_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int64_t]], bool) nogil
      vector[One_critical_filtration[int64_t]]& get_filtrations() nogil
      C_Slicer_Matrix0_i32 coarsen_on_grid(vector[vector[int64_t]]) nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[vector[int64_t]]) nogil
      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[pair[vector[int64_t],vector[int64_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_Matrix1_i64 "TrucPythonInterface<BackendsEnum::Matrix,false,false,int64_t,Available_columns::SMALL_VECTOR>":
      ctypedef int64_t value_type

      C_Slicer_Matrix1_i64()

      C_Slicer_Matrix1_i64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[int64_t]]&)

      C_Slicer_Matrix1_i64& operator=(const C_Slicer_Matrix1_i64&)
      vector[vector[pair[int64_t, int64_t]]] get_barcode() nogil
      void push_to(const Line[int64_t]&) nogil
      void set_one_filtration(const vector[int64_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int64_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int64_t], One_critical_filtration[int64_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int64_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int64_t]], bool) nogil
      vector[One_critical_filtration[int64_t]]& get_filtrations() nogil
      C_Slicer_Matrix1_i32 coarsen_on_grid(vector[vector[int64_t]]) nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[vector[int64_t]]) nogil
      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[pair[vector[int64_t],vector[int64_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_Matrix0_f32 "TrucPythonInterface<BackendsEnum::Matrix,false,false,float,Available_columns::INTRUSIVE_SET>":
      ctypedef float value_type

      C_Slicer_Matrix0_f32()

      C_Slicer_Matrix0_f32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[float]]&)

      C_Slicer_Matrix0_f32& operator=(const C_Slicer_Matrix0_f32&)
      vector[vector[pair[float, float]]] get_barcode() nogil
      void push_to(const Line[float]&) nogil
      void set_one_filtration(const vector[float]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[float] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[float], One_critical_filtration[float]] get_bounding_box() except + nogil
      vector[One_critical_filtration[float]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[float]], bool) nogil
      vector[One_critical_filtration[float]]& get_filtrations() nogil
      C_Slicer_Matrix0_i32 coarsen_on_grid(vector[vector[float]]) nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[vector[float]]) nogil
      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[pair[vector[float],vector[float]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_Matrix1_f32 "TrucPythonInterface<BackendsEnum::Matrix,false,false,float,Available_columns::SMALL_VECTOR>":
      ctypedef float value_type

      C_Slicer_Matrix1_f32()

      C_Slicer_Matrix1_f32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[float]]&)

      C_Slicer_Matrix1_f32& operator=(const C_Slicer_Matrix1_f32&)
      vector[vector[pair[float, float]]] get_barcode() nogil
      void push_to(const Line[float]&) nogil
      void set_one_filtration(const vector[float]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[float] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[float], One_critical_filtration[float]] get_bounding_box() except + nogil
      vector[One_critical_filtration[float]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[float]], bool) nogil
      vector[One_critical_filtration[float]]& get_filtrations() nogil
      C_Slicer_Matrix1_i32 coarsen_on_grid(vector[vector[float]]) nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[vector[float]]) nogil
      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[pair[vector[float],vector[float]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_Matrix0_f64 "TrucPythonInterface<BackendsEnum::Matrix,false,false,double,Available_columns::INTRUSIVE_SET>":
      ctypedef double value_type

      C_Slicer_Matrix0_f64()

      C_Slicer_Matrix0_f64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[double]]&)

      C_Slicer_Matrix0_f64& operator=(const C_Slicer_Matrix0_f64&)
      vector[vector[pair[double, double]]] get_barcode() nogil
      void push_to(const Line[double]&) nogil
      void set_one_filtration(const vector[double]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[double] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[double], One_critical_filtration[double]] get_bounding_box() except + nogil
      vector[One_critical_filtration[double]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[double]], bool) nogil
      vector[One_critical_filtration[double]]& get_filtrations() nogil
      C_Slicer_Matrix0_i32 coarsen_on_grid(vector[vector[double]]) nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[vector[double]]) nogil
      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[pair[vector[double],vector[double]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_Matrix1_f64 "TrucPythonInterface<BackendsEnum::Matrix,false,false,double,Available_columns::SMALL_VECTOR>":
      ctypedef double value_type

      C_Slicer_Matrix1_f64()

      C_Slicer_Matrix1_f64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[double]]&)

      C_Slicer_Matrix1_f64& operator=(const C_Slicer_Matrix1_f64&)
      vector[vector[pair[double, double]]] get_barcode() nogil
      void push_to(const Line[double]&) nogil
      void set_one_filtration(const vector[double]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[double] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[double], One_critical_filtration[double]] get_bounding_box() except + nogil
      vector[One_critical_filtration[double]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[double]], bool) nogil
      vector[One_critical_filtration[double]]& get_filtrations() nogil
      C_Slicer_Matrix1_i32 coarsen_on_grid(vector[vector[double]]) nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[vector[double]]) nogil
      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[pair[vector[double],vector[double]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_GudhiCohomology0_i32 "TrucPythonInterface<BackendsEnum::GudhiCohomology,false,true,int32_t,Available_columns::INTRUSIVE_SET>":
      ctypedef int32_t value_type

      C_KSlicer_GudhiCohomology0_i32()

      C_KSlicer_GudhiCohomology0_i32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[int32_t]]&)

      C_KSlicer_GudhiCohomology0_i32& operator=(const C_KSlicer_GudhiCohomology0_i32&)
      vector[vector[pair[int32_t, int32_t]]] get_barcode() nogil
      void push_to(const Line[int32_t]&) nogil
      void set_one_filtration(const vector[int32_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int32_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int32_t], One_critical_filtration[int32_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int32_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int32_t]], bool) nogil
      vector[Multi_critical_filtration[int32_t]]& get_filtrations() nogil
      C_KSlicer_GudhiCohomology0_i32 coarsen_on_grid(vector[vector[int32_t]]) nogil
      void add_generator(const One_critical_filtration[int32_t] &) nogil


      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[vector[int32_t]]) nogil
      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[pair[vector[int32_t],vector[int32_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_GudhiCohomology0_i64 "TrucPythonInterface<BackendsEnum::GudhiCohomology,false,true,int64_t,Available_columns::INTRUSIVE_SET>":
      ctypedef int64_t value_type

      C_KSlicer_GudhiCohomology0_i64()

      C_KSlicer_GudhiCohomology0_i64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[int64_t]]&)

      C_KSlicer_GudhiCohomology0_i64& operator=(const C_KSlicer_GudhiCohomology0_i64&)
      vector[vector[pair[int64_t, int64_t]]] get_barcode() nogil
      void push_to(const Line[int64_t]&) nogil
      void set_one_filtration(const vector[int64_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int64_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int64_t], One_critical_filtration[int64_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int64_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int64_t]], bool) nogil
      vector[Multi_critical_filtration[int64_t]]& get_filtrations() nogil
      C_KSlicer_GudhiCohomology0_i32 coarsen_on_grid(vector[vector[int64_t]]) nogil
      void add_generator(const One_critical_filtration[int64_t] &) nogil


      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[vector[int64_t]]) nogil
      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[pair[vector[int64_t],vector[int64_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_GudhiCohomology0_f32 "TrucPythonInterface<BackendsEnum::GudhiCohomology,false,true,float,Available_columns::INTRUSIVE_SET>":
      ctypedef float value_type

      C_KSlicer_GudhiCohomology0_f32()

      C_KSlicer_GudhiCohomology0_f32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[float]]&)

      C_KSlicer_GudhiCohomology0_f32& operator=(const C_KSlicer_GudhiCohomology0_f32&)
      vector[vector[pair[float, float]]] get_barcode() nogil
      void push_to(const Line[float]&) nogil
      void set_one_filtration(const vector[float]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[float] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[float], One_critical_filtration[float]] get_bounding_box() except + nogil
      vector[One_critical_filtration[float]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[float]], bool) nogil
      vector[Multi_critical_filtration[float]]& get_filtrations() nogil
      C_KSlicer_GudhiCohomology0_i32 coarsen_on_grid(vector[vector[float]]) nogil
      void add_generator(const One_critical_filtration[float] &) nogil


      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[vector[float]]) nogil
      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[pair[vector[float],vector[float]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_KSlicer_GudhiCohomology0_f64 "TrucPythonInterface<BackendsEnum::GudhiCohomology,false,true,double,Available_columns::INTRUSIVE_SET>":
      ctypedef double value_type

      C_KSlicer_GudhiCohomology0_f64()

      C_KSlicer_GudhiCohomology0_f64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[Multi_critical_filtration[double]]&)

      C_KSlicer_GudhiCohomology0_f64& operator=(const C_KSlicer_GudhiCohomology0_f64&)
      vector[vector[pair[double, double]]] get_barcode() nogil
      void push_to(const Line[double]&) nogil
      void set_one_filtration(const vector[double]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[double] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[double], One_critical_filtration[double]] get_bounding_box() except + nogil
      vector[One_critical_filtration[double]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[double]], bool) nogil
      vector[Multi_critical_filtration[double]]& get_filtrations() nogil
      C_KSlicer_GudhiCohomology0_i32 coarsen_on_grid(vector[vector[double]]) nogil
      void add_generator(const One_critical_filtration[double] &) nogil


      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[vector[double]]) nogil
      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[pair[vector[double],vector[double]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_GudhiCohomology0_i32 "TrucPythonInterface<BackendsEnum::GudhiCohomology,false,false,int32_t,Available_columns::INTRUSIVE_SET>":
      ctypedef int32_t value_type

      C_Slicer_GudhiCohomology0_i32()

      C_Slicer_GudhiCohomology0_i32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[int32_t]]&)

      C_Slicer_GudhiCohomology0_i32& operator=(const C_Slicer_GudhiCohomology0_i32&)
      vector[vector[pair[int32_t, int32_t]]] get_barcode() nogil
      void push_to(const Line[int32_t]&) nogil
      void set_one_filtration(const vector[int32_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int32_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int32_t], One_critical_filtration[int32_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int32_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int32_t]], bool) nogil
      vector[One_critical_filtration[int32_t]]& get_filtrations() nogil
      C_Slicer_GudhiCohomology0_i32 coarsen_on_grid(vector[vector[int32_t]]) nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[vector[int32_t]]) nogil
      vector[vector[vector[pair[int32_t, int32_t]]]] persistence_on_lines(vector[pair[vector[int32_t],vector[int32_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_GudhiCohomology0_i64 "TrucPythonInterface<BackendsEnum::GudhiCohomology,false,false,int64_t,Available_columns::INTRUSIVE_SET>":
      ctypedef int64_t value_type

      C_Slicer_GudhiCohomology0_i64()

      C_Slicer_GudhiCohomology0_i64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[int64_t]]&)

      C_Slicer_GudhiCohomology0_i64& operator=(const C_Slicer_GudhiCohomology0_i64&)
      vector[vector[pair[int64_t, int64_t]]] get_barcode() nogil
      void push_to(const Line[int64_t]&) nogil
      void set_one_filtration(const vector[int64_t]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[int64_t] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[int64_t], One_critical_filtration[int64_t]] get_bounding_box() except + nogil
      vector[One_critical_filtration[int64_t]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[int64_t]], bool) nogil
      vector[One_critical_filtration[int64_t]]& get_filtrations() nogil
      C_Slicer_GudhiCohomology0_i32 coarsen_on_grid(vector[vector[int64_t]]) nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[vector[int64_t]]) nogil
      vector[vector[vector[pair[int64_t, int64_t]]]] persistence_on_lines(vector[pair[vector[int64_t],vector[int64_t]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_GudhiCohomology0_f32 "TrucPythonInterface<BackendsEnum::GudhiCohomology,false,false,float,Available_columns::INTRUSIVE_SET>":
      ctypedef float value_type

      C_Slicer_GudhiCohomology0_f32()

      C_Slicer_GudhiCohomology0_f32(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[float]]&)

      C_Slicer_GudhiCohomology0_f32& operator=(const C_Slicer_GudhiCohomology0_f32&)
      vector[vector[pair[float, float]]] get_barcode() nogil
      void push_to(const Line[float]&) nogil
      void set_one_filtration(const vector[float]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[float] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[float], One_critical_filtration[float]] get_bounding_box() except + nogil
      vector[One_critical_filtration[float]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[float]], bool) nogil
      vector[One_critical_filtration[float]]& get_filtrations() nogil
      C_Slicer_GudhiCohomology0_i32 coarsen_on_grid(vector[vector[float]]) nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[vector[float]]) nogil
      vector[vector[vector[pair[float, float]]]] persistence_on_lines(vector[pair[vector[float],vector[float]]]) nogil

#------------------------------------------------------------------------------
cdef extern from "Persistence_slices_interface.h":
  cdef cppclass C_Slicer_GudhiCohomology0_f64 "TrucPythonInterface<BackendsEnum::GudhiCohomology,false,false,double,Available_columns::INTRUSIVE_SET>":
      ctypedef double value_type

      C_Slicer_GudhiCohomology0_f64()

      C_Slicer_GudhiCohomology0_f64(const vector[vector[unsigned int]]&, const vector[int]&, const vector[One_critical_filtration[double]]&)

      C_Slicer_GudhiCohomology0_f64& operator=(const C_Slicer_GudhiCohomology0_f64&)
      vector[vector[pair[double, double]]] get_barcode() nogil
      void push_to(const Line[double]&) nogil
      void set_one_filtration(const vector[double]&) nogil
      int prune_above_dimension(int) except + nogil 

      vector[double] get_one_filtration()
      # void compute_persistence(vector[bool]) except+ nogil
      void compute_persistence(bool) except+ nogil # ignore_inf
      void compute_persistence() except+ nogil # ignore_inf
      uint32_t num_generators() nogil
      uint32_t num_parameters() nogil
      string to_str() nogil
      pair[One_critical_filtration[double], One_critical_filtration[double]] get_bounding_box() except + nogil
      vector[One_critical_filtration[double]] get_filtration_values() nogil
      vector[int] get_dimensions() nogil
      vector[vector[uint]] get_boundaries() nogil
      void coarsen_on_grid_inplace(vector[vector[double]], bool) nogil
      vector[One_critical_filtration[double]]& get_filtrations() nogil
      C_Slicer_GudhiCohomology0_i32 coarsen_on_grid(vector[vector[double]]) nogil
      void build_from_scc_file(const string&, bool, bool, int) except + nogil
      void write_to_scc_file(const string&, int, int, bool, bool, bool, bool) nogil


      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[vector[double]]) nogil
      vector[vector[vector[pair[double, double]]]] persistence_on_lines(vector[pair[vector[double],vector[double]]]) nogil



#### MMA Stuff

from multipers.mma_structures cimport Module
cdef extern from "multiparameter_module_approximation/approximation.h" namespace "Gudhi::multiparameter::mma":
  Module[float] multiparameter_module_approximation(C_KSlicer_Matrix0_vine_f32&, One_critical_filtration[float]&, float, Box[float]&, bool, bool, bool) except + nogil
  Module[float] multiparameter_module_approximation(C_KSlicer_Matrix1_vine_f32&, One_critical_filtration[float]&, float, Box[float]&, bool, bool, bool) except + nogil
  Module[double] multiparameter_module_approximation(C_KSlicer_Matrix0_vine_f64&, One_critical_filtration[double]&, double, Box[double]&, bool, bool, bool) except + nogil
  Module[double] multiparameter_module_approximation(C_KSlicer_Matrix1_vine_f64&, One_critical_filtration[double]&, double, Box[double]&, bool, bool, bool) except + nogil
  Module[float] multiparameter_module_approximation(C_Slicer_Matrix0_vine_f32&, One_critical_filtration[float]&, float, Box[float]&, bool, bool, bool) except + nogil
  Module[float] multiparameter_module_approximation(C_Slicer_Matrix1_vine_f32&, One_critical_filtration[float]&, float, Box[float]&, bool, bool, bool) except + nogil
  Module[double] multiparameter_module_approximation(C_Slicer_Matrix0_vine_f64&, One_critical_filtration[double]&, double, Box[double]&, bool, bool, bool) except + nogil
  Module[double] multiparameter_module_approximation(C_Slicer_Matrix1_vine_f64&, One_critical_filtration[double]&, double, Box[double]&, bool, bool, bool) except + nogil




import multipers.slicer as mps
from cython.operator cimport dereference
cdef inline Module[double] _multiparameter_module_approximation_f64(object slicer, One_critical_filtration[double] direction, double max_error, Box[double] box, bool threshold, bool complete, bool verbose):
  import multipers.slicer as mps
  cdef intptr_t slicer_ptr = <intptr_t>(slicer.get_ptr())
  cdef Module[double] mod
  if False:
    pass
  elif isinstance(slicer, mps._KSlicer_Matrix0_vine_f64):
    with nogil:
      mod = multiparameter_module_approximation(dereference(<C_KSlicer_Matrix0_vine_f64*>(slicer_ptr)), direction, max_error, box, threshold, complete, verbose)
    return mod
  elif isinstance(slicer, mps._KSlicer_Matrix1_vine_f64):
    with nogil:
      mod = multiparameter_module_approximation(dereference(<C_KSlicer_Matrix1_vine_f64*>(slicer_ptr)), direction, max_error, box, threshold, complete, verbose)
    return mod
  elif isinstance(slicer, mps._Slicer_Matrix0_vine_f64):
    with nogil:
      mod = multiparameter_module_approximation(dereference(<C_Slicer_Matrix0_vine_f64*>(slicer_ptr)), direction, max_error, box, threshold, complete, verbose)
    return mod
  elif isinstance(slicer, mps._Slicer_Matrix1_vine_f64):
    with nogil:
      mod = multiparameter_module_approximation(dereference(<C_Slicer_Matrix1_vine_f64*>(slicer_ptr)), direction, max_error, box, threshold, complete, verbose)
    return mod
  else:
    raise ValueError(f"Unsupported slicer type {type(slicer)}")
cdef inline Module[float] _multiparameter_module_approximation_f32(object slicer, One_critical_filtration[float] direction, float max_error, Box[float] box, bool threshold, bool complete, bool verbose):
  import multipers.slicer as mps
  cdef intptr_t slicer_ptr = <intptr_t>(slicer.get_ptr())
  cdef Module[float] mod
  if False:
    pass
  elif isinstance(slicer, mps._KSlicer_Matrix0_vine_f32):
    with nogil:
      mod = multiparameter_module_approximation(dereference(<C_KSlicer_Matrix0_vine_f32*>(slicer_ptr)), direction, max_error, box, threshold, complete, verbose)
    return mod
  elif isinstance(slicer, mps._KSlicer_Matrix1_vine_f32):
    with nogil:
      mod = multiparameter_module_approximation(dereference(<C_KSlicer_Matrix1_vine_f32*>(slicer_ptr)), direction, max_error, box, threshold, complete, verbose)
    return mod
  elif isinstance(slicer, mps._Slicer_Matrix0_vine_f32):
    with nogil:
      mod = multiparameter_module_approximation(dereference(<C_Slicer_Matrix0_vine_f32*>(slicer_ptr)), direction, max_error, box, threshold, complete, verbose)
    return mod
  elif isinstance(slicer, mps._Slicer_Matrix1_vine_f32):
    with nogil:
      mod = multiparameter_module_approximation(dereference(<C_Slicer_Matrix1_vine_f32*>(slicer_ptr)), direction, max_error, box, threshold, complete, verbose)
    return mod
  else:
    raise ValueError(f"Unsupported slicer type {type(slicer)}")

###### RANK INVARIANT
from libc.stdint cimport intptr_t, uint16_t, uint32_t, int32_t, int16_t, int8_t
ctypedef int32_t tensor_dtype
ctypedef int32_t indices_type
python_indices_type=np.int32
python_tensor_dtype = np.int32



ctypedef pair[vector[vector[indices_type]], vector[tensor_dtype]] signed_measure_type



cdef extern from "multi_parameter_rank_invariant/rank_invariant.h" namespace "Gudhi::multiparameter::rank_invariant":
  ## from slicers
    void compute_rank_invariant_python(C_KSlicer_Matrix0_vine_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_Matrix0_vine_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_Matrix1_vine_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_Matrix1_vine_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_Matrix0_vine_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_Matrix0_vine_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_Matrix1_vine_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_Matrix1_vine_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_Matrix0_vine_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_Matrix0_vine_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_Matrix1_vine_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_Matrix1_vine_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_Matrix0_vine_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_Matrix0_vine_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_Matrix1_vine_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_Matrix1_vine_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_Matrix0_vine_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_Matrix0_vine_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_Matrix1_vine_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_Matrix1_vine_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_Matrix0_vine_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_Matrix0_vine_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_Matrix1_vine_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_Matrix1_vine_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_Matrix0_vine_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_Matrix0_vine_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_Matrix1_vine_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_Matrix1_vine_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_Matrix0_vine_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_Matrix0_vine_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_Matrix1_vine_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_Matrix1_vine_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_Matrix0_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_Matrix0_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_Matrix1_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_Matrix1_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_Matrix0_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_Matrix0_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_Matrix1_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_Matrix1_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_Matrix0_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_Matrix0_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_Matrix1_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_Matrix1_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_Matrix0_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_Matrix0_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_Matrix1_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_Matrix1_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_Matrix0_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_Matrix0_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_Matrix1_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_Matrix1_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_Matrix0_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_Matrix0_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_Matrix1_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_Matrix1_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_Matrix0_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_Matrix0_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_Matrix1_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_Matrix1_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_Matrix0_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_Matrix0_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_Matrix1_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_Matrix1_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_GudhiCohomology0_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_GudhiCohomology0_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_GudhiCohomology0_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_GudhiCohomology0_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_GudhiCohomology0_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_GudhiCohomology0_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_KSlicer_GudhiCohomology0_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_KSlicer_GudhiCohomology0_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_GudhiCohomology0_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_GudhiCohomology0_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_GudhiCohomology0_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_GudhiCohomology0_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_GudhiCohomology0_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_GudhiCohomology0_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil
    void compute_rank_invariant_python(C_Slicer_GudhiCohomology0_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool ignore_inf) except + nogil
    signed_measure_type compute_rank_signed_measure(C_Slicer_GudhiCohomology0_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type], indices_type, bool verbose, bool ignore_inf) except + nogil





cdef inline void _compute_rank_invariant(object slicer, tensor_dtype* container_ptr, vector[indices_type] c_grid_shape, vector[indices_type] degrees, int n_jobs, bool ignore_inf):
  import multipers.slicer as mps
  cdef intptr_t slicer_ptr = <intptr_t>(slicer.get_ptr())
  if isinstance(slicer, mps._KSlicer_Matrix0_vine_i32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_Matrix0_vine_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_Matrix1_vine_i32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_Matrix1_vine_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_Matrix0_vine_i64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_Matrix0_vine_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_Matrix1_vine_i64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_Matrix1_vine_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_Matrix0_vine_f32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_Matrix0_vine_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_Matrix1_vine_f32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_Matrix1_vine_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_Matrix0_vine_f64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_Matrix0_vine_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_Matrix1_vine_f64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_Matrix1_vine_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_Matrix0_vine_i32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_Matrix0_vine_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_Matrix1_vine_i32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_Matrix1_vine_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_Matrix0_vine_i64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_Matrix0_vine_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_Matrix1_vine_i64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_Matrix1_vine_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_Matrix0_vine_f32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_Matrix0_vine_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_Matrix1_vine_f32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_Matrix1_vine_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_Matrix0_vine_f64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_Matrix0_vine_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_Matrix1_vine_f64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_Matrix1_vine_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_Matrix0_i32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_Matrix0_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_Matrix1_i32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_Matrix1_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_Matrix0_i64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_Matrix0_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_Matrix1_i64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_Matrix1_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_Matrix0_f32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_Matrix0_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_Matrix1_f32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_Matrix1_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_Matrix0_f64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_Matrix0_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_Matrix1_f64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_Matrix1_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_Matrix0_i32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_Matrix0_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_Matrix1_i32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_Matrix1_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_Matrix0_i64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_Matrix0_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_Matrix1_i64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_Matrix1_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_Matrix0_f32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_Matrix0_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_Matrix1_f32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_Matrix1_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_Matrix0_f64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_Matrix0_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_Matrix1_f64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_Matrix1_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_GudhiCohomology0_i32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_GudhiCohomology0_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_GudhiCohomology0_i64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_GudhiCohomology0_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_GudhiCohomology0_f32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_GudhiCohomology0_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._KSlicer_GudhiCohomology0_f64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_KSlicer_GudhiCohomology0_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_GudhiCohomology0_i32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_GudhiCohomology0_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_GudhiCohomology0_i64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_GudhiCohomology0_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_GudhiCohomology0_f32):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_GudhiCohomology0_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  if isinstance(slicer, mps._Slicer_GudhiCohomology0_f64):
    with nogil:
      compute_rank_invariant_python(dereference(<C_Slicer_GudhiCohomology0_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs,ignore_inf)
      return
  raise ValueError(f"Unsupported slicer type {type(slicer)}")



cdef inline  _compute_rank_sm(object slicer, tensor_dtype* container_ptr, vector[indices_type] c_grid_shape, vector[indices_type] degrees, int n_jobs, bool verbose, bool ignore_inf):
  import multipers.slicer as mps
  cdef intptr_t slicer_ptr = <intptr_t>(slicer.get_ptr())
  cdef signed_measure_type sm
  cdef cnp.ndarray[indices_type, ndim=2] pts
  cdef cnp.ndarray[tensor_dtype, ndim=1] weights
  if isinstance(slicer, mps._KSlicer_Matrix0_vine_i32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_Matrix0_vine_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix1_vine_i32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_Matrix1_vine_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix0_vine_i64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_Matrix0_vine_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix1_vine_i64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_Matrix1_vine_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix0_vine_f32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_Matrix0_vine_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix1_vine_f32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_Matrix1_vine_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix0_vine_f64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_Matrix0_vine_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix1_vine_f64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_Matrix1_vine_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix0_vine_i32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_Matrix0_vine_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix1_vine_i32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_Matrix1_vine_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix0_vine_i64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_Matrix0_vine_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix1_vine_i64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_Matrix1_vine_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix0_vine_f32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_Matrix0_vine_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix1_vine_f32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_Matrix1_vine_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix0_vine_f64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_Matrix0_vine_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix1_vine_f64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_Matrix1_vine_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix0_i32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_Matrix0_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix1_i32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_Matrix1_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix0_i64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_Matrix0_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix1_i64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_Matrix1_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix0_f32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_Matrix0_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix1_f32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_Matrix1_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix0_f64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_Matrix0_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix1_f64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_Matrix1_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix0_i32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_Matrix0_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix1_i32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_Matrix1_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix0_i64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_Matrix0_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix1_i64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_Matrix1_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix0_f32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_Matrix0_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix1_f32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_Matrix1_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix0_f64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_Matrix0_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix1_f64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_Matrix1_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_GudhiCohomology0_i32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_GudhiCohomology0_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_GudhiCohomology0_i64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_GudhiCohomology0_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_GudhiCohomology0_f32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_GudhiCohomology0_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_GudhiCohomology0_f64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_KSlicer_GudhiCohomology0_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_GudhiCohomology0_i32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_GudhiCohomology0_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_GudhiCohomology0_i64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_GudhiCohomology0_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_GudhiCohomology0_f32):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_GudhiCohomology0_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_GudhiCohomology0_f64):
    with nogil:
      sm = compute_rank_signed_measure(dereference(<C_Slicer_GudhiCohomology0_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  raise ValueError(f"Unsupported slicer type {type(slicer)}")



#### Hilbert Function

cdef extern from "multi_parameter_rank_invariant/hilbert_function.h" namespace "Gudhi::multiparameter::hilbert_function":
  ## from slicers
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_Matrix0_vine_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_Matrix1_vine_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_Matrix0_vine_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_Matrix1_vine_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_Matrix0_vine_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_Matrix1_vine_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_Matrix0_vine_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_Matrix1_vine_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_Matrix0_vine_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_Matrix1_vine_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_Matrix0_vine_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_Matrix1_vine_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_Matrix0_vine_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_Matrix1_vine_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_Matrix0_vine_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_Matrix1_vine_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_Matrix0_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_Matrix1_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_Matrix0_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_Matrix1_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_Matrix0_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_Matrix1_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_Matrix0_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_Matrix1_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_Matrix0_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_Matrix1_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_Matrix0_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_Matrix1_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_Matrix0_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_Matrix1_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_Matrix0_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_Matrix1_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_GudhiCohomology0_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_GudhiCohomology0_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_GudhiCohomology0_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_KSlicer_GudhiCohomology0_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_GudhiCohomology0_i32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_GudhiCohomology0_i64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_GudhiCohomology0_f32&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
    signed_measure_type get_hilbert_signed_measure(C_Slicer_GudhiCohomology0_f64&, tensor_dtype* , const vector[indices_type], const vector[indices_type],  bool zero_pad,indices_type n_jobs, bool verbose, bool ignore_inf) except + nogil
cdef inline  _compute_hilbert_sm(object slicer, tensor_dtype* container_ptr, vector[indices_type] c_grid_shape, vector[indices_type] degrees, int n_jobs, bool verbose,bool zero_pad, bool ignore_inf):
  import multipers.slicer as mps
  cdef intptr_t slicer_ptr = <intptr_t>(slicer.get_ptr())
  cdef signed_measure_type sm
  cdef cnp.ndarray[indices_type, ndim=2] pts
  cdef cnp.ndarray[tensor_dtype, ndim=1] weights
  if isinstance(slicer, mps._KSlicer_Matrix0_vine_i32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_Matrix0_vine_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix1_vine_i32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_Matrix1_vine_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix0_vine_i64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_Matrix0_vine_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix1_vine_i64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_Matrix1_vine_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix0_vine_f32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_Matrix0_vine_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix1_vine_f32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_Matrix1_vine_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix0_vine_f64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_Matrix0_vine_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix1_vine_f64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_Matrix1_vine_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix0_vine_i32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_Matrix0_vine_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix1_vine_i32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_Matrix1_vine_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix0_vine_i64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_Matrix0_vine_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix1_vine_i64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_Matrix1_vine_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix0_vine_f32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_Matrix0_vine_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix1_vine_f32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_Matrix1_vine_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix0_vine_f64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_Matrix0_vine_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix1_vine_f64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_Matrix1_vine_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix0_i32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_Matrix0_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix1_i32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_Matrix1_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix0_i64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_Matrix0_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix1_i64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_Matrix1_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix0_f32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_Matrix0_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix1_f32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_Matrix1_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix0_f64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_Matrix0_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_Matrix1_f64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_Matrix1_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix0_i32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_Matrix0_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix1_i32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_Matrix1_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix0_i64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_Matrix0_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix1_i64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_Matrix1_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix0_f32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_Matrix0_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix1_f32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_Matrix1_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix0_f64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_Matrix0_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_Matrix1_f64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_Matrix1_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_GudhiCohomology0_i32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_GudhiCohomology0_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_GudhiCohomology0_i64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_GudhiCohomology0_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_GudhiCohomology0_f32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_GudhiCohomology0_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._KSlicer_GudhiCohomology0_f64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_KSlicer_GudhiCohomology0_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_GudhiCohomology0_i32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_GudhiCohomology0_i32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_GudhiCohomology0_i64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_GudhiCohomology0_i64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_GudhiCohomology0_f32):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_GudhiCohomology0_f32*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  if isinstance(slicer, mps._Slicer_GudhiCohomology0_f64):
    with nogil:
      sm = get_hilbert_signed_measure(dereference(<C_Slicer_GudhiCohomology0_f64*>(slicer_ptr)),container_ptr, c_grid_shape,degrees, zero_pad, n_jobs, verbose, ignore_inf)
    pts = np.asarray(sm.first,dtype=python_indices_type)
    weights = np.asarray(sm.second,dtype=python_tensor_dtype)
    return (pts,weights)
  raise ValueError(f"Unsupported slicer type {type(slicer)}")
