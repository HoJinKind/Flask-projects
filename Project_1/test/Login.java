package Project;


import java.util.concurrent.TimeUnit;
import org.junit.*;
import static org.junit.Assert.*;

import org.openqa.selenium.*;
import org.openqa.selenium.firefox.FirefoxDriver;



public class Login {
  private WebDriver driver;
  private StringBuffer verificationErrors = new StringBuffer();

  @Before
  public void setUp() throws Exception {
    driver = new FirefoxDriver();
    driver.manage().timeouts().implicitlyWait(30, TimeUnit.SECONDS);
  }

  @Test
  public void testUntitledTestCase() throws Exception {
	String user = "tom";
	String pwd= "sutd1234";
    driver.get("http://35.198.199.181:5000/");
    driver.findElement(By.name("username")).click();
    driver.findElement(By.name("username")).clear();
    driver.findElement(By.name("username")).sendKeys(user);
    assertEquals ("tom", user);
    driver.findElement(By.name("pd")).clear();
    driver.findElement(By.name("pd")).sendKeys(pwd);
    assertEquals ("sutd1234", pwd);
    driver.findElement(By.name("pd")).sendKeys(Keys.ENTER);
    
    Thread.sleep(2000);
    assertEquals ("home", driver.getTitle());
  }

  @After
  public void tearDown() throws Exception {
    driver.quit();
    String verificationErrorString = verificationErrors.toString();
    if (!"".equals(verificationErrorString)) {
      fail(verificationErrorString);
    }
  }

}
