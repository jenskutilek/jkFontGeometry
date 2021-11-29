#[test]
fn test_intersect() {
    assert_eq!(pyext-fastgeometry::intersect((0.0, 0.0), (0.0, 10.0), (-1.0, 5.0), (1.0, 5.0)), [0.0, 5.0]);
}